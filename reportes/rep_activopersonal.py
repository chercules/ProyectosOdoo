from odoo import api, models


class ParticularReport(models.AbstractModel):
    _name = 'report.module.report_name'
    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('module.report_name')

        custom_data = self.env['model.name'].get_data()

        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
            'custom_data': custom_data,
        }
        return report_obj.render('module.report_name', docargs)