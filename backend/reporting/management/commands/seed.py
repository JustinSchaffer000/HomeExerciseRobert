import datetime
from django.core.management.base import BaseCommand
from faker import Faker
from itertools import groupby
from progress.bar import Bar
from random import choice, randrange, sample, uniform
from reporting.models import *
import pytz


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.fake = Faker()
        self.vendors = [Business(name=self.fake.company()) for _ in range(3)]
        for vendor in self.vendors:
            vendor.save()
        bar = Bar('Seeding', max=100)
        for _ in range(100):
            self.seed_customer()
            bar.next()
        bar.finish()
        self.stdout.write('Done.')

    def seed_customer(self):
        customer = Business(name=self.fake.company())
        customer.save()
        jobs = [self.seed_job(customer) for _ in range(3)]
        [self.seed_invoice(customer, jobs) for _ in range(3)]
        return customer

    def seed_job(self, customer):
        job = Job(business=customer, name=self.fake.bs())
        job.save()
        return job

    def seed_invoice(self, customer, jobs):
        vendor = choice(self.vendors)
        invoice = Invoice(
            business=vendor,
            number=self.fake.numerify(text='!!###'),
            due_date=pytz.utc.localize(
                self.fake.date_time_this_year(after_now=True)),
            status=choice([Invoice.DRAFT, Invoice.PAID, Invoice.UNPAID]),
        )
        invoice.save()

        invoice_line_items_with_nones = [self.seed_invoice_line_item(
            jobs, invoice) in range(randrange(100))]
        invoice_line_items = [
            x for x in invoice_line_items_with_nones if x != None]
        items_to_be_paid = sample(
            invoice_line_items, int(len(invoice_line_items) / 2))
        self.pay_line_items(customer, items_to_be_paid)

        return invoice

    def seed_invoice_line_item(self, jobs, invoice):
        job = choice(jobs)
        amount = uniform(0, 1000)
        job_line_item = LineItem(
            job=job, description=self.fake.bs(), amount=amount)
        job_line_item.save()

        if randrange(0, 10) < 5:
            invoice_line_item = LineItem(
                invoice=invoice, self_item=job_line_item, description=self.fake.bs(), amount=amount)
            invoice_line_item.save()
            return invoice_line_item
        else:
            return None

    def pay_line_items(self, customer, items_to_be_paid):
        def keyfunc(x): return x.invoice
        for invoice, invoice_line_items in groupby(items_to_be_paid, keyfunc):
            payment_type = choice(
                [Payment.CHECK, Payment.DEBIT_CARD, Payment.CREDIT_CARD])
            amount = sum([x.amount for x in invoice_line_items])
            initiated_date = pytz.utc.localize(
                self.fake.date_time_this_year(after_today=True))
            completed_date = initiated_date + datetime.timedelta(days=7)
            payment = Payment(payer=customer,
                              payee=invoice.business,
                              amount=amount,
                              reference=self.fake.numerify(text='!!###'),
                              payment_type=payment_type,
                              initiated_at=initiated_date,
                              completed_at=completed_date,
                              )
            payment.save()

            for invoice_line_item in invoice_line_items:
                line_item = LineItem(
                    payment=payment,
                    self_item=invoice_line_item,
                    description=invoice_line_item.description,
                    amount=invoice_line_item.amount,
                )
                line_item.save()
