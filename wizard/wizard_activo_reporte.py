# -*- coding: utf-8 -*-

import xlwt
import datetime
import unicodedata
import base64
import io
from io import BytesIO
import csv
# import cStringIO
from datetime import datetime
from odoo import models, fields, api


class activofijosv_reportes(models.TransientModel):
    _name = "activofijosv.reportes"
    _description = 'Reporte de Activos Fijos'

    #titulo = fields.Char('Titulo')
    titulo = fields.Char(string="Titulo", help="Ingrese la serie de activo si aplica")
    descripcion = fields.Text('Descripcion')
    fechaini = fields.Date('Fecha Inicial', Required=True)
    fechafin = fields.Date('Fecha Final',Required=True)

   # @api.multi
    def accion_reporte(self):
        """CODIGO DEL REPORTE"""

        datas = {'ids': self.env.context.get('active_ids', [])}
        res = self.read(['titulo', 'descripcion', 'fechaini','fechafin'])
        res = res and res[0] or {}
        #res['titulo'] = res['titulo'][0]
        datas['form'] = res

        return self.env.ref('activofijosv.action_reporte_all_activos').report_action([], data=datas)

    #Clase para ventana de descarga de Excel
    class ExcelReportOut(models.TransientModel):
        _name = 'excel.report.out'
        _description = 'Reporte Excel'

        reportexls_data = fields.Char('Name', size=256)
        file_name = fields.Binary('Reporte Excel', readonly=True)



    # purchase order excel report button actions
   # @api.multi
    def exportar_reporte(self):

        # XLS report
        libro = xlwt.Workbook()

        #Definiendo Estilos
        style0 = xlwt.easyxf('font: name Times New Roman bold on;align: horiz right;', num_format_str='#,##0.00')
        style1 = xlwt.easyxf(
            'font: name Times New Roman bold on; pattern: pattern solid, fore_colour black;align: horiz center;',
            num_format_str='#,##0.00')
        style2 = xlwt.easyxf('font:height 400,bold True; pattern: pattern solid, fore_colour black;',
                             num_format_str='#,##0.00')
        style3 = xlwt.easyxf('font:bold True;', num_format_str='#,##0.00')
        style4 = xlwt.easyxf('font:bold True;  borders:top double;align: horiz right;', num_format_str='#,##0.00')
        style5 = xlwt.easyxf('font: name Times New Roman bold on;align: horiz center;', num_format_str='#,##0')
        style6 = xlwt.easyxf('font: name Times New Roman bold on;', num_format_str='#,##0.00')
        style7 = xlwt.easyxf('font:bold True;  borders:top double;', num_format_str='#,##0.00')
        #Fin de Estilos

        hoja = libro.add_sheet("Hoja1")


        cols = ["A", "B", "C", "D", "E"]
        txt = "Fila %s, Columna %s"

        #for num in range(5):
        #    row = hoja.row(num)
        #    for index, col in enumerate(cols):
        #        value = txt % (num + 1, col)
        #        row.write(index, value)
        #self._agregar_estilo_hoja(libro, "EstiloHoja")

        #Leyendo datos
        domain = []
        # self.fch_findepre = datetime.strptime(self.fch_inidepre, "%Y-%m-%d")
        domain = [('create_date', '>=', self.fechaini),
                  ('create_date', '<=', self.fechafin)]

    #    print domain
        fields = ['name','correlativo','fecha_compra','estado','costo','tipo_activo','rubro_id','categoria_id','subcategoria_id','departamento_id','ubicacion_id','fch_inidepre','depreciaporcen','create_date','vidautilmeses','vidautilanos','activousado_id','valestimadonew','valoradpreciar','valoresiduo','dpreciaxmes','serie','marca','placa','codigo_alterno','fecha_baja','empleado_id']
        wdatos = self.env['activofijosv.activo'].search_read(domain, fields)

        #activosf = self.env['activofijosv.activo'].browse(self._context.get('active_ids', list()))
        #order = self.env['purchase.order'].browse(self._context.get('active_ids', list()))

        #Encabezados de Reportes

        hoja.write_merge(0, 0, 6, 10, 'REPORTE DE ACTIVO FIJO')
        #Encabezados de Registros
        hoja.write(1, 0, 'No',style1)
        hoja.write(1, 1, 'Codigo', style1)
        hoja.write(1, 2, 'Nombre', style1)
        hoja.write(1, 3, 'Fecha Compra', style1)
        hoja.write(1, 4, 'Estado', style1)
        hoja.write(1, 5, 'Tipo Activo', style1)
        hoja.write(1, 6, 'Costo', style1)
        hoja.write(1, 7, 'Rubro', style1)
        hoja.write(1, 8, 'Categoria', style1)
        hoja.write(1, 9, 'Subcategoria', style1)
        hoja.write(1, 10, 'Departamento', style1)
        hoja.write(1, 11, 'Ubicacion', style1)
        hoja.write(1, 12, 'Inicio Depreciacion', style1)
        hoja.write(1, 13, '% Depreciacion', style1)
        hoja.write(1, 14, 'Vida Util Meses', style1)
        hoja.write(1, 15, 'Vida Util Anos ', style1)
        hoja.write(1, 16, 'Antiguiedad Anos ', style1)
        hoja.write(1, 17, 'Valor Estimado ', style1)
        hoja.write(1, 18, 'Valor a Depreciar ', style1)
        hoja.write(1, 19, 'Valor Residual', style1)
        hoja.write(1, 20, 'Depreciacion Mensual', style1)
        hoja.write(1, 21, 'Meses depreciados', style1)
        hoja.write(1, 22, 'Depreciacion Acumulada', style1)
        hoja.write(1, 23, 'Serie', style1)
        hoja.write(1, 24, 'Marca', style1)
        hoja.write(1, 25, 'Placa', style1)
        hoja.write(1, 26, 'Codigo Alterno', style1)
        hoja.write(1, 27, 'Fecha de Baja', style1)
        hoja.write(1, 28, 'Empleado', style1)
        hoja.write(1, 29, 'Fecha Creacion', style1)


        x = 2
        for rec in wdatos:

            #Registros
            hoja.write(x, 0, x-1)

            hoja.write(x, 1, rec['correlativo'])
            hoja.write(x, 2,rec['name'])
            hoja.write(x, 3, rec['fecha_compra'])
            if rec['estado']=='0':
                hoja.write(x, 4, 'Nuevo')
            else:
                hoja.write(x, 4, 'Usado')

            if rec['tipo_activo']=='0':
                hoja.write(x, 5, 'Activo Fijo')
            else:
                hoja.write(x, 5, 'Resultado')

            hoja.write(x, 6, rec['costo'],style3)
            hoja.write(x, 7, rec['rubro_id'][1])
            hoja.write(x, 8, rec['categoria_id'][1])
            hoja.write(x, 9, rec['subcategoria_id'][1])
            hoja.write(x, 10, rec['departamento_id'][1])
            hoja.write(x, 11,rec['ubicacion_id'][1])
            hoja.write(x, 12, rec['fch_inidepre'])
            hoja.write(x, 13, rec['depreciaporcen'])
            hoja.write(x, 14, rec['vidautilmeses'])
            hoja.write(x, 15, rec['vidautilanos'])
            if rec['activousado_id']:
                hoja.write(x, 16, rec['activousado_id'][1])
            else:
                hoja.write(x, 16, ' ')
            hoja.write(x, 17, rec['valestimadonew'])
            hoja.write(x, 18, rec['valoradpreciar'])
            hoja.write(x, 19, rec['valoresiduo'])
            hoja.write(x, 20, rec['dpreciaxmes'])
            hoja.write(x, 21, self._depreciacionacu(rec['fch_inidepre'],self.fechafin))
            hoja.write(x, 22, self._depreciacionacu(rec['fch_inidepre'], self.fechafin) * rec['dpreciaxmes'])
            hoja.write(x, 23, rec['serie'])
            hoja.write(x, 24, rec['marca'])
            hoja.write(x, 25, rec['placa'])
            hoja.write(x, 26, rec['codigo_alterno'])
            hoja.write(x, 27, rec['fecha_baja'])
            if rec['empleado_id']:
                hoja.write(x, 28, rec['empleado_id'][1])
            else:
                hoja.write(x, 28, ' ')
            hoja.write(x, 29, rec['create_date'])

            x=x+1

       # hoja.write_merge(0,1, 2, 6, 'Reporte de Activo Fijo :', style2)
        #hoja.write_merge(2, 3, 7, 8, 12354, style2)

       # hoja.write(5, 1, 'Vendor5')


        libro.save("/tmp/Reporte Activos.xls")

        #Generando ventana para atachar el excel
        fp = open("/tmp/Reporte Activos.xls", "rb")
        file_data = fp.read()
        out = base64.encodestring(file_data)

        # Files actions
        attach_vals = {
            'reportexls_data': 'Reporte Activos.xls',
            'file_name': out,

        }

        act_id = self.env['excel.report.out'].create(attach_vals)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'excel.report.out',
            'res_id': act_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'context': self.env.context,
            'target': 'new',
        }

    def _agregar_estilo_hoja(self,libro, nombre):

        valor = "Este es el estilo de hoja!"
        hoja = libro.add_sheet(nombre)
        style = 'pattern: pattern solid, fore_colour blue;'
        hoja.row(0).write(0, valor, xlwt.Style.easyxf(style))

    def _depreciacionacu(self,fechainicial,fechafinal):

        valor = "Este es el estilo de hoja!"

        diaini=datetime.strptime(fechainicial, "%Y-%m-%d").day
        mesini=datetime.strptime(fechainicial, "%Y-%m-%d").month
        anoini=datetime.strptime(fechainicial, "%Y-%m-%d").year

        diafin = datetime.strptime(fechafinal, "%Y-%m-%d").day
        mesfin = datetime.strptime(fechafinal, "%Y-%m-%d").month
        anofin = datetime.strptime(fechafinal, "%Y-%m-%d").year

        difano=anofin-anoini
        difmes=mesfin-mesini
        #print mesfin


        if difano>0:
            tmes=difano*12+difmes
        else:
            tmes=difmes


        return tmes


