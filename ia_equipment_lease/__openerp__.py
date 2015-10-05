# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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


{
    'name': 'IA Equipment Tracking System',
    'version': '1.0',
    'category': 'Information Systems/Equipment Management',
    'description': """
The base module to manage equipment leasing.
======================================================
Developed for Servtel Solutions Limited
""",
    'author': 'Intellect Alliance Limited',
    'website': 'http://www.intellectalliance.com',
    'depends': ['account','product', 'sale', 'project'],
    'data': [
        'ia_equipment_lease_view.xml',
    ],
    'demo': [],
    'test':[],
    'installable': True,
    'application': True,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
