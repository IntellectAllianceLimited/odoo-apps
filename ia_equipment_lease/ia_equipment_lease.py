# Name: Intellect Alliance Equipment Management Module
# Desc: Equipment 1.0 Module in OpenERP MVC,
# File name: ia_equipment_lease.py
# Developed by: Kingsley Ndiewo
# Date: 17/08/2014
# Place: Nairobi, Kenya

# external libraries
# -------------------------------------------------
import logging
from datetime import datetime, date
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

# the type of tool; a hierarchy can be created
class ia_tool_type(osv.osv):
    _name = 'ia.tool.type'
    _description = 'IA Tool Type'
    _rec_name = 'tt_name'
    _columns = {
        'tt_name': fields.char('Tool Type', size=32, required=True),
        'tt_description': fields.text('Description', help="The description for this type of tool"),
        'tt_parent_id': fields.many2one('ia.tool.type', 'Parent Type', select=True, ondelete='cascade', help="The parent type for this type of tool")
    }
    _order = 'tt_name'

# the tool record
class ia_tool_tool(osv.osv):
    _name = 'ia.tool.tool'
    _rec_name = 'tool_name'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'IA Tool Record'
    _columns = {
        'tool_name': fields.char('Name', size=70, required=True, help="The name of the tool"),
        'tool_desc': fields.text('Description', help="The description for this tool"),
        'tool_type': fields.many2one('ia.tool.type', 'Type', required=True, help="The type of tool"),
        'tool_code': fields.char('Code', size=25, required=True, help="The unique code for this tool"),
        'tool_available': fields.selection([('available', 'Available'), ('borrowed', 'Borrowed'), ('lost', 'Lost'),
            ('damage', 'Damaged')], 'Availability', required=True, help="Availability of the tool currently"),
        'tool_product' : fields.many2one('product.product', 'Tool Product', help="The product associated with this tool"),
    }
    _defaults = {
        'tool_available': 'available',
    }
    _order = 'tool_name'

# a tool request by an engineer
class ia_tool_request(osv.osv):
    def action_approve_request(self, cr, uid, ids, context=None):
        # tool must be available but just check
        request_obj = self.pool.get('ia.tool.request').browse(cr, uid, ids[0])
        if request_obj.tr_tool.tool_available != 'available':
            # prompt unavailable
            raise osv.except_osv(_('Warning !'),_("The tool %s is unavailable!") % (request_obj.tr_tool.tool_name,))
        else:
            # generate a lease document
            vals = {'lease_responsible' : request_obj.tr_requester.id, 'lease_tool' : request_obj.tr_tool.id}
            self.pool.get('ia.tool.lease').create(cr, uid, vals)
            raise osv.except_osv(_('Information!'),_("The lease for %s has been created!") % (request_obj.tr_tool.tool_name,))
    
    def create(self, cr, uid, vals, context=None):
        """ Overrides orm create method to check tool availability """
        # get the tool
        tool_obj = self.pool.get('ia.tool.tool').browse(cr, uid, vals['tr_tool'])
        if tool_obj.tool_available != 'available':
            # prompt unavailable
            raise osv.except_osv(_('Warning !'),_("The tool %s is unavailable!") % (tool_obj.tool_name,))
        else:
            result = super(ia_tool_request, self).create(cr, uid, vals, context=context)
            return result
            
    _name = 'ia.tool.request'
    _description = 'IA Tool Request'
    _rec_name = 'tr_code'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _columns = {
        'tr_code': fields.char('Code', size=25, required=True, help="The unique code for this tool request"),
        'tr_requester': fields.many2one('res.users', 'Requested By', required=True, help="Person borrowing for this tool"),
        'tr_tool': fields.many2one('ia.tool.tool', 'Tool', required=True, help="The tool to be requested"),
        'tr_date': fields.date('Request Date', required=True, help="Date and time of request"),
        'tr_state': fields.selection([('approved', 'Approved'), ('pending', 'Pending'), ('denied', 'Denied')], 'Status', readonly=True)
    }
    _defaults = {
        # uses the sequences object to generate a sequence for this object; ensure the sequence exists
        'tr_code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'ia.tool.request'),
        'tr_date': datetime.now().strftime('%Y-%m-%d'),
        'tr_state': 'pending'
    }
    _order = 'tr_code'

# the lease record
class ia_tool_lease(osv.osv):
    _name = 'ia.tool.lease'
    _rec_name = 'lease_code'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'IA Tool Lease'
    _columns = {
        'lease_code': fields.char('Code', size=25, required=True, help="The unique code for this lease transaction"),
        'lease_responsible': fields.many2one('res.users', 'Responsible', required=True, help="Person borrowing this tool"),
        'lease_date': fields.datetime('Lease Date', required=True, help="Date and time of borrowing"),
        'lease_due': fields.datetime('Lease Due', help="Date and time due for return"),
        'lease_project': fields.many2one('project.project', 'Project', help="The project associated with this lease"),
        'lease_tool': fields.many2one('ia.tool.tool', 'Tool', required=True, help="The tool borrowed in this lease"),
        'lease_state': fields.selection([('done', 'Done'), ('process', 'Ongoing'), ('overdue', 'Overdue'),
            ('dispute', 'Dispute')], 'State', required=True, help="The state of the lease"), 
        }
    _defaults = {
        # uses the sequences object to generate a sequence for this object; ensure the sequence exists
        'lease_code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'ia.tool.lease'),
        'lease_state': 'process',
        'lease_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    _order = 'lease_code'    