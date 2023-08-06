# -*- coding: utf-8 -*-
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.exceptions import Warning as UserError
from openerp.addons.l10n_it_fatturapa_pec.tests.e_invoice_common \
    import EInvoiceCommon


class TestEInvoiceSend(EInvoiceCommon):

    def setUp(self):
        super(TestEInvoiceSend, self).setUp()

    def test_send_check_fetchmail(self):
        """Sending e-invoice when there is no
        PEC server configured raises UserError"""
        e_invoice = self._create_e_invoice()

        # There is no PEC server configured
        with self.assertRaises(UserError):
            e_invoice.send_via_pec()

    def test_send(self):
        """Sending e-invoice changes its state to 'sent'"""
        e_invoice = self._create_e_invoice()

        self._create_fetchmail_pec_server()
        e_invoice.send_via_pec()
        self.assertEqual(e_invoice.state, 'sent')

    def test_wizard_send(self):
        """Sending e-invoice with wizard changes its state to 'sent'"""
        e_invoice = self._create_e_invoice()

        self._create_fetchmail_pec_server()
        wiz = self.env['wizard.fatturapa.send.pec'].create({})
        wiz.with_context(active_ids=e_invoice.ids).send_pec()
        self.assertEqual(e_invoice.state, 'sent')

    def test_resend_reset(self):
        """Re-sending e-invoice raises UserError"""
        e_invoice = self._create_e_invoice()

        self._create_fetchmail_pec_server()
        e_invoice.send_via_pec()
        self.assertEqual(e_invoice.state, 'sent')

        # Cannot re-send e-invoice whose state is 'sent'
        with self.assertRaises(UserError):
            e_invoice.send_via_pec()

        # Cannot reset e-invoice whose state is 'sent'
        with self.assertRaises(UserError):
            e_invoice.reset_to_ready()
