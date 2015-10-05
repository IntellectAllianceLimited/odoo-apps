# Name: Intellect Alliance Tenders Management Module
# Desc: Tenders 1.0 Module in OpenERP MVC,
# File name: ia_tenders.py
# Developed by: Kingsley Ndiewo
# Date: 17/08/2014
# Place: Nairobi, Kenya

# external libraries
# -------------------------------------------------
import logging
from datetime import datetime
import time
# -------------------------------------------------
# import essential Odoo libraries
from openerp.osv import fields, osv
import openerp
from openerp import tools
from openerp.tools.translate import _
# -------------------------------------------------
# logging alias
_logger = logging.getLogger(__name__)
# -------------------------------------------------

# the type of tender; a hierarchy can be created
class ia_tender_type(osv.osv):
    _name = 'ia.tender.type'
    _description = 'IA Tender Type'
    _rec_name = 'tt_name'
    _columns = {
        'tt_name': fields.char('Tender Type', size=32, required=True),
        'tt_description': fields.text('Description', help="The description for this type of tender"),
        'tt_parent_id': fields.many2one('ia.tender.type', 'Parent Type', select=True, ondelete='cascade', help="The parent type for this type of tender")
    }
    _order = 'tt_name'

# tender site visits or meetings
class ia_tender_activity(osv.osv):
    _name = 'ia.tender.activity'
    _rec_name = 'ta_name'
    _description = 'IA Tender Activity'
    _columns = {
        'ta_name': fields.char('Meeting Name', size=50, required=True),
        'ta_tender': fields.many2one('ia.tender.tender', 'Tender', help="The tender associated with this meeting or visit"),
        'ta_description': fields.text('Description', help="The description for this meeting or visit"),
        'ta_date': fields.datetime('Date and Time', help="Date and time of the meeting or visit"),
        'ta_resolutions': fields.text('Resolutions', help="The resolutions of this meeting or visit"),
    }
    _order = 'ta_name'

# inherit document and extend
class ia_document(osv.osv):
    _inherit = 'ir.attachment'
    _columns = {
        'tender_id': fields.many2one('ia.tender.tender', 'Tender', help="The tender associated with this document"),
    }

# inherit and extend sale order class 
class sale_order(osv.osv):
    _inherit = "sale.order"
    _columns = {
        'tender_id': fields.many2one('ia.tender.tender', 'Tender'),
    }

# the tender record
class ia_tender_tender(osv.osv):
    _name = 'ia.tender.tender'
    _rec_name = 'tender_code'
    _description = 'IA Tender Record'
    _columns = {
        'tender_title': fields.char('Title', size=150, required=True, help="The title of the tender"),
        'tender_desc': fields.text('Description', help="The description for this tender"),
        'tender_type': fields.many2one('ia.tender.type', 'Type', help="The type of tender"),
        'tender_code': fields.char('Code', size=25, required=True, help="The unique code for this tender"),
        'tender_fee' : fields.float('Purchase Fee', help="The cost of the tender document"),
        'tender_expiry': fields.datetime('Expiry Date/Time', required=True, help="The date and time for expiry of the tender"),
        'tender_documents': fields.one2many('ir.attachment', 'tender_id', 'Documents', help="The documents associated with this tender"),
        'tender_quotes' : fields.one2many('sale.order', 'tender_id', "Quotations/Orders", help="The quotations / orders linked to this tender"),
        'tender_results': fields.selection([('pending', 'Pending'), ('awarded', 'Awarded'), ('cancelled', 'Cancelled'),
            ('failed', 'Unsuccessful')], 'Results', help="The tender results"),
        'tender_activities': fields.one2many('ia.tender.activity', 'ta_tender', 'Meetings / Site Vists', help="The meetings and visits associated with this tender"),
        'tender_state': fields.selection([
            ('draft', 'Draft Tender'),
            ('sent', 'Tender Sent'),
            ('cancel', 'Tender Cancelled'),
            ('waiting_date', 'Waiting Schedule'),
            ('prequalify', 'Pre-Qualified'),
            ('award', 'Awarded'),
            ('progress', 'In Progress'),
            ('done', 'Done'),
            ], 'Status', help="Gives the status of the tender"),
        'tender_responsible': fields.many2one('res.users', 'Responsible', help="Person responsible for this tender"),
        'tender_punctual': fields.boolean('Punctual', help="Was the tender handed in on time?"),
    }
    _order = 'tender_title'