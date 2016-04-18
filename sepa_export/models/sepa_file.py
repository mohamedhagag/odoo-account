# -*- encoding: utf-8 -*-
##############################################################################
#
#    UNamur - University of Namur, Belgium (www.unamur.be)
#    Copyright (C) UNamur <http://www.unamur.be>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, exceptions
import logging

_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _inherit = "account.payment"

    sepa_file_id = fields.Many2one('account.sepa_file', string="SEPA File", readonly=True)
    partner_bank_id = fields.Many2one('res.partner.bank', string="Partner bank account",
                                      domain="[('partner_id','=',partner_id)")

    @api.one
    @api.constrains('partner_bank_id', 'payment_method_id')
    def _partner_bank_required(self):
        """Ensure the partner bank account is set for payments using the SEPA method
        """
        for payment in self:
            if payment.payment_method_code == "SEPA" and not(payment.partner_bank_id):
                raise exceptions.ValidationError(_("The partner bank account is mandatory when using the SEPA method"))


class SEPAFile(models.Model):
    _name = 'account.sepa_file'

    name = fields.Char(string='Reference', size=35, readonly=True, required=True)
    date = fields.Datetime(string='Creation Date', readonly=True, required=True)
    xml_file = fields.Binary("File", attachment=True, help="The SEPA file", readonly=True)
    payment_ids = fields.One2many("account.payment", "sepa_file_id", "Activities", readonly=True)

    _order = "date desc"
