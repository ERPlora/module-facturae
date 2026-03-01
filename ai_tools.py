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
