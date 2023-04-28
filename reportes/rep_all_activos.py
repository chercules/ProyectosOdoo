# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import float_round


class report_activofijosv_allactivos(models.AbstractModel):
    _name = "report.activofijosv.reporte_all_activos"

    @api.model
    def get_report_values(self, docids, data=None):

        data = data if data is not None else {}

        #wdatos = self.env['activofijosv.activo'].browse(data.get('form', {}).get('titulo', False))
        domain = []
        #self.fch_findepre = datetime.strptime(self.fch_inidepre, "%Y-%m-%d")
        domain = [('create_date', '>=', data.get('form').get('fechaini')),('create_date', '<=', data.get('form').get('fechafin'))]

        fields = ['name', 'create_date', 'rubro_id']
        wdatos = self.env['activofijosv.activo'].search_read(domain, fields)

        activosf  = self.env['activofijosv.activo'].browse(data.get('ids', data.get('active_ids')))

        return {
            'doc_ids': data.get('ids', data.get('active_ids')),
            'doc_model': 'activofijosv.activo',
            'docs': activosf,
            'data': dict(
                data,
                activo_data=wdatos,
            ),
        }

"""
          data = data if data is not None else {}
          data = self.env['activofijosv.activo'].get_data()

          activosf = self.env['activofijosv.activo'].browse(data.get('ids',data.get('active_ids')))
          docargs ={
              'doc_ids' : data.get('ids',data.get('active_ids')),
              'doc_model' : 'activofijosv.activo',
              'docs' : activosf,
              'data' : dict(data),
            }
          return self.env['report'].render('activofijosv.reporte_all_activos',docargs)
"""

