from .models import Business, LineItem
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json

def Custormer(request):
    customers = Business.objects.select_related('Job__LineItem').values('name', 'job__name', 'job__lineitem__amount')
    customer_job_amount = {}
    for customer in customers:
        if customer['name'] not in customer_job_amount:
            customer_job_amount[customer['name']] = {
                'name': customer['name'],
                'amount': 0
            }
        amount = 0
        if customer['job__lineitem__amount'] != None:
            amount = customer['job__lineitem__amount']

        customer_job_amount[customer['name']] = {
            'name': customer['name'],
            'amount': customer_job_amount[customer['name']]['amount'] + amount
        }

    invoices = LineItem.objects.raw('select li.id, li.invoice_id as id, b.name as name, li.amount as amount from reporting_lineitem as li ' + \
                                    'left join reporting_lineitem as l on l.id = li.self_item_id ' + \
                                    'left join reporting_job as j on l.job_id = j.id ' + \
                                    'left join reporting_business as b on j.business_id = b.id ' + \
                                    'where b.name is not null')
    customer_invoices = {}
    for invoice in invoices:
        if invoice.name not in customer_invoices:
            customer_invoices[invoice.name] = {
                'id': [],
                'amount': 0
            }
        customer_invoices[invoice.name] = {
            'id': customer_invoices[invoice.name]['id'] + [invoice.id],
            'amount': customer_invoices[invoice.name]['amount'] + invoice.amount
        }
    
    payments = LineItem.objects.raw('SELECT l.invoice_id AS id, p.reference AS reference, p.payment_type AS type, SUM(l.amount) AS amount ' + \
                                    'FROM reporting_lineitem AS l ' + \
                                    'LEFT JOIN reporting_payment AS p ON l.payment_id = p.id ' + \
                                    'WHERE p.reference IS NOT NULL ' + \
                                    'GROUP BY l.invoice_id, p.reference, p.payment_type ')
    invoice_payments = {}
    for payment in payments:
        invoice_payments[payment.id] = {
            'reference': payment.reference,
            'type': payment.type,
            'amount': payment.amount
        }
    
    return JsonResponse({ "customer": customer_job_amount, "customer_invoices": customer_invoices, "invoice_payments": invoice_payments }, safe=False)
    