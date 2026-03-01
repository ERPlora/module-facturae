"""AI tools for the FacturaE module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListFacturaeInvoices(AssistantTool):
    name = "list_facturae_invoices"
    description = "List FacturaE electronic invoices."
    module_id = "facturae"
    required_permission = "facturae.view_facturaeinvoice"
    parameters = {"type": "object", "properties": {"status": {"type": "string", "description": "draft, generated, submitted, accepted, rejected"}, "limit": {"type": "integer"}}, "required": [], "additionalProperties": False}

    def execute(self, args, request):
        from facturae.models import FacturaeInvoice
        qs = FacturaeInvoice.objects.all()
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        limit = args.get('limit', 20)
        return {"invoices": [{"id": str(i.id), "invoice_number": i.invoice_number, "recipient_name": i.recipient_name, "total_amount": str(i.total_amount), "status": i.status} for i in qs.order_by('-created_at')[:limit]]}


@register_tool
class GetFacturaeInvoice(AssistantTool):
    name = "get_facturae_invoice"
    description = "Get detailed FacturaE invoice info including XML generation and submission timestamps."
    module_id = "facturae"
    required_permission = "facturae.view_facturaeinvoice"
    parameters = {
        "type": "object",
        "properties": {"invoice_id": {"type": "string", "description": "Invoice ID"}},
        "required": ["invoice_id"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from facturae.models import FacturaeInvoice
        i = FacturaeInvoice.objects.get(id=args['invoice_id'])
        return {
            "id": str(i.id), "invoice_number": i.invoice_number,
            "recipient_name": i.recipient_name, "recipient_tax_id": i.recipient_tax_id,
            "total_amount": str(i.total_amount), "status": i.status,
            "xml_generated_at": i.xml_generated_at.isoformat() if i.xml_generated_at else None,
            "submitted_at": i.submitted_at.isoformat() if i.submitted_at else None,
            "response_code": i.response_code if i.response_code else None,
        }


@register_tool
class CreateFacturaeInvoice(AssistantTool):
    name = "create_facturae_invoice"
    description = "Create a draft FacturaE electronic invoice."
    module_id = "facturae"
    required_permission = "facturae.add_facturaeinvoice"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "invoice_number": {"type": "string", "description": "Invoice number"},
            "recipient_name": {"type": "string", "description": "Recipient company/person name"},
            "recipient_tax_id": {"type": "string", "description": "Recipient tax ID (NIF/CIF)"},
            "total_amount": {"type": "string", "description": "Total invoice amount"},
        },
        "required": ["invoice_number", "recipient_name", "recipient_tax_id", "total_amount"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from decimal import Decimal
        from facturae.models import FacturaeInvoice
        i = FacturaeInvoice.objects.create(
            invoice_number=args['invoice_number'],
            recipient_name=args['recipient_name'],
            recipient_tax_id=args['recipient_tax_id'],
            total_amount=Decimal(args['total_amount']),
            status='draft',
        )
        return {"id": str(i.id), "invoice_number": i.invoice_number, "status": "draft", "created": True}


@register_tool
class UpdateFacturaeStatus(AssistantTool):
    name = "update_facturae_status"
    description = "Update FacturaE invoice status: generate (draft→generated), submit (generated→submitted)."
    module_id = "facturae"
    required_permission = "facturae.change_facturaeinvoice"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "invoice_id": {"type": "string", "description": "Invoice ID"},
            "action": {"type": "string", "description": "Action: generate, submit"},
        },
        "required": ["invoice_id", "action"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from django.utils import timezone
        from facturae.models import FacturaeInvoice
        i = FacturaeInvoice.objects.get(id=args['invoice_id'])
        action = args['action']
        if action == 'generate' and i.status == 'draft':
            i.status = 'generated'
            i.xml_generated_at = timezone.now()
            i.save(update_fields=['status', 'xml_generated_at'])
        elif action == 'submit' and i.status == 'generated':
            i.status = 'submitted'
            i.submitted_at = timezone.now()
            i.save(update_fields=['status', 'submitted_at'])
        else:
            return {"error": f"Cannot {action} a {i.status} invoice"}
        return {"id": str(i.id), "invoice_number": i.invoice_number, "status": i.status}
