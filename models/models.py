# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, time, timedelta
import calendar

class activofijosv_activo(models.Model):
    _name = "activofijosv.activo"

    #Calcula la fecha de Inicio de depreciacion asumiendo fecha de compra por default hoy
    @api.model
    def _fecha_depreciar(self):
        finicial = date.today().replace(day=1, month=date.today().month, year=date.today().year)

        if date.today().day<=15:
               finicial= date.today().replace(day=1, month=date.today().month, year=date.today().year)
        else:
                if date.today().month==12:
                    finicial = date.today().replace(day=1, month=1 ,year=date.today().year+1)
                else:
                    finicial = date.today().replace(day=1, month=date.today().month+1,year=date.today().year)
        return  finicial



    name = fields.Char(string="Nombre",required=True,help="Ingresa el nombre del Activo a Inventariar")
    descripcion = fields.Text(string="Descripcion",help="Ingrese la descripcion del activo")
    serie = fields.Char(string="Serie",help="Ingrese la serie de activo si aplica")
    marca = fields.Char(string="Marca", help="Ingrese la Marca de activo si aplica")
    modelo = fields.Char(string="Modelo", help="Ingrese el modelo del activo que ingresa, si aplica") #Modelo del activo, Estradaj
    fecha_compra = fields.Date(string="Fecha de compra",required=True,help="Ingrese la fecha de compra del Activo",default=fields.Date.context_today )
    fecha_baja = fields.Date(string ="Fecha de baja",help="Ingrese la fecha en que se dio de baja a este bien")
    costo = fields.Float(string="Costo",help="Ingrese el costo de adquisicion del activo")
    placa = fields.Char(string="Placa", help="Ingrese la placa del activo si aplica")
    proveedor = fields.Char(string="Proveedor", help="Ingrese el nombre del lugar donde se compro el activo") #Proveedor del activo, Estradaj
    codigo_alterno = fields.Char(string="Codigo Alterno",help="Ingrese un codigo personalizado si aplica")
    estado = fields.Selection([('0','Nuevo'),('1','Usado')],string="Estado",default="0",help="El Activo es nuevo o Usado")
    tipo_activo = fields.Selection([('0','Activo Fijo'),('1','Resultados'),('2','Otro')],string="Tipo de Activo",default="0",help="Activo Fijo se deprecia, Resultados van al gasto")
    rubro_id     = fields.Many2one("activofijosv.rubros", string="Rubro",required=True)
    categoria_id = fields.Many2one("activofijosv.categoria", string="Categoria", required=True)
    subcategoria_id = fields.Many2one("activofijosv.subcategoria", string="SubCategoria", required=True)
    ubicacion_id = fields.Many2one("activofijosv.ubicacion", string="Ubicacion", required=True)
    empleado_id = fields.Many2one("hr.employee", string="Empleado")
    departamento_id = fields.Many2one("hr.department", string="Departamento", required=True)
    codbarra = fields.Char(string="Codigo de Barra", compute="_codactivo", store=True)
    correlativo = fields.Char(string="Consecutivo", compute="_consecutivo", store=True)
    depreciaporcen = fields.Float(string="Depreciacion %",help="Porcentaje de depreciacion del bien")
    vidautilanos = fields.Float(string="Vida Util Anos",compute="_recalvidautil", store=True)
    vidautilmeses = fields.Float(string="Vida Util Meses",compute="_recalvidautil", store=True)
    fch_inidepre = fields.Date(string="Fecha depreciacion", help="Fecha en que se inicio a depreciar este bien",default=_fecha_depreciar)
    fch_findepre = fields.Date(string="Fecha Vencimiento", help="Fecha en que se termino de depreciar el bien")
    valoresiduo = fields.Float(string="Valor Residual", help="Valor Residual que resta al costo del bien")
    valoradpreciar=fields.Float(string ="Valor a depreciar")
    dpreciaxmes = fields.Float(string="Depreciacion Mensual",help="Monto de depreciacion mensual", compute="_recalvidautil", store=True)
    valestimadonew = fields.Float(string="Valor Estimado",help="Valor estimado del bien usado cuando se compro nuevo")
    activousado_id = fields.Many2one("activofijosv.usados", string="Antiguedad en anos" ,help="Antiguedad de bien cuando se compra usado")
    imagen = fields.Binary()

   # @api.multi
    @api.depends("ubicacion_id")
    def _codactivo(self):
        for r in self:
            prefijocia = self.env['res.company'].search([('prefijocompany', '!=', '')], limit=1).prefijocompany
            r.codbarra=  str(prefijocia)+ str(r.ubicacion_id.prefijoubicacion + r.departamento_id.prefijodepto + r.rubro_id.prefijorubro + r.categoria_id.prefijocategoria + r.subcategoria_id.prefijosubcategoria)


    #@api.multi
    @api.depends("ubicacion_id")
    def _consecutivo(self):
        for r in self:
            prefijocia = self.env['res.company'].search([('prefijocompany', '!=', '')], limit=1).prefijocompany
            codigoprincipal = str(prefijocia) + str(r.ubicacion_id.prefijoubicacion + r.departamento_id.prefijodepto + r.rubro_id.prefijorubro + r.categoria_id.prefijocategoria + r.subcategoria_id.prefijosubcategoria)
            consecutivo = str(self.env['activofijosv.activo'].search_count([('codbarra', '=', codigoprincipal)]) + 1).zfill(3)
            r.correlativo =  str(codigoprincipal) + consecutivo

    #Calcula la Fecha de Incio y Fin de la depreciacion
    @api.onchange('rubro_id')
    def _fechavence(self):
        if self.rubro_id:
            if self.rubro_id.depreciaminima==0:
                self.fch_findepre = datetime.strptime(self.fch_inidepre, "%Y-%m-%d")
            else:
                vidautil=int(((1 / self.rubro_id.depreciaminima)) * 100)
                self.fch_findepre= datetime.strptime(self.fch_inidepre, "%Y-%m-%d").replace(day=datetime.strptime(self.fch_inidepre, "%Y-%m-%d").day, month=datetime.strptime(self.fch_inidepre, "%Y-%m-%d").month,year=datetime.strptime(self.fch_inidepre, "%Y-%m-%d").year+vidautil)
            self.depreciaporcen=self.rubro_id.depreciaminima
            self.vidautilanos = vidautil
            self.vidautilmeses = vidautil*12
            self.dpreciaxmes = (self.costo-self.valoresiduo)/(vidautil*12)

        # Calcula vida Util si se cambia el porcentaje de deprecacion

    #@api.multi
    @api.depends('depreciaporcen')
    def _recalvidautil(self):
        if self.depreciaporcen:
            if self.depreciaporcen <= 0:
                    self.fch_findepre = datetime.strptime(self.fch_inidepre, "%Y-%m-%d")
            else:
                 vidautil = int(((1 / self.depreciaporcen)) * 100)
                 self.fch_findepre = datetime.strptime(self.fch_inidepre, "%Y-%m-%d").replace(
                        day=datetime.strptime(self.fch_inidepre, "%Y-%m-%d").day,
                        month=datetime.strptime(self.fch_inidepre, "%Y-%m-%d").month,
                        year=datetime.strptime(self.fch_inidepre, "%Y-%m-%d").year + vidautil)

            self.vidautilanos = vidautil
            self.vidautilmeses = vidautil * 12
            self.dpreciaxmes = (self.costo - self.valoresiduo) / (vidautil * 12)




    # Calcula Valor a depreciar depreciacion

    @api.onchange('estado')
    def _valoradepre(self):
        if self.estado:
            if self.estado=='0':
                self.valoradpreciar=self.costo
#

    @api.onchange('valoresiduo')
    def _depremen(self):
        self._recalvidautil()


    #Calcula el valor a depreciar
    @api.onchange('valestimadonew')
    def _costodepre(self):
        if self.valestimadonew:
            maximoadeducir=0
            if self.estado == '1':
                maximoadeducir=(self.env['activofijosv.usados'].search([('name', '=', self.activousado_id.name)], limit=1).porcentaje/100)*self.valestimadonew
                if self.costo<maximoadeducir:
                    self.valoradpreciar = self.costo
                else:
                    self.valoradpreciar=maximoadeducir
            else:
                self.valoradpreciar = maximoadeducir

    @api.onchange('costo')
    def _valoradepre(self):
        if self.costo:
            if self.estado == '0':
                self.valoradpreciar = self.costo
        self._recalvidautil()

    ######## Si se modifica la fecha de compra recalcula la fecha inicial de dpreciacion
    @api.onchange('fecha_compra')
    def _fecha_deprecia(self):
        if self.fecha_compra:
            finicial = datetime.strptime(self.fecha_compra, "%Y-%m-%d").replace(day=1, month=datetime.strptime(self.fecha_compra, "%Y-%m-%d").month, year=datetime.strptime(self.fecha_compra, "%Y-%m-%d").year)

            if datetime.strptime(self.fecha_compra, "%Y-%m-%d").day<=15:
                   finicial= datetime.strptime(self.fecha_compra, "%Y-%m-%d").replace(day=1, month=datetime.strptime(self.fecha_compra, "%Y-%m-%d").month, year=datetime.strptime(self.fecha_compra, "%Y-%m-%d").year)
            else:
                    if datetime.strptime(self.fecha_compra, "%Y-%m-%d").month==12:
                        finicial = datetime.strptime(self.fecha_compra, "%Y-%m-%d").replace(day=1, month=1 ,year=datetime.strptime(self.fecha_compra, "%Y-%m-%d").year+1)
                    else:
                        finicial = datetime.strptime(self.fecha_compra, "%Y-%m-%d").replace(day=1, month=datetime.strptime(self.fecha_compra, "%Y-%m-%d").month+1,year=datetime.strptime(self.fecha_compra, "%Y-%m-%d").year)
            self.fch_inidepre=finicial



#

class activofijosv_rubros(models.Model):
    _name="activofijosv.rubros"

    name = fields.Char(string="Rubro",required=True,help="Nombre del Rubro")
    activorub_id = fields.One2many("activofijosv.activo","rubro_id",string="Activos fijos")

    prefijorubro = fields.Char(string="Prefijo Activo Fijo",required=True,size=2,help="Codigo de 2 Digitos que representa el Rubro en el codigo de Barra")
    depreciaminima = fields.Float(string="Depreciacion %",required=True,help="Porcentaje minimo de deprecacion de ley")
    vidautil = fields.Float(string="Vida Util Anos", compute="_vidautil2", store=True)
    vidautilmes = fields.Float(string="Vida Util Meses", compute="_vidautilmes", store=True)

    #@api.multi
    @api.depends("depreciaminima")
    def _vidautil2(self):
        for r in self:
            if r.depreciaminima > 0:
                r.vidautil = int((1/r.depreciaminima)*100)
            else:
                r.vidautil=0

    @api.depends("depreciaminima")
    def _vidautilmes(self):
        for r in self:
            if r.depreciaminima > 0:
                r.vidautilmes = int((1/r.depreciaminima)*100)*12
            else:
                r.vidautilmes=0


class activofijoch_categoria(models.Model):
    _name = "activofijosv.categoria"

    name = fields.Char(string="Categoria",required=True,help="Ingrese nombre de categoria")
    activocat_id = fields.One2many("activofijosv.activo", "categoria_id", string="Activos fijos")
    rubro_id = fields.Many2one("activofijosv.rubros", string="Rubros", required=True)
    prefijocategoria = fields.Char(string="Prefijo Activo Fijo", required=True,size=2,help="Codigo de 2 Digitos que representa la categoria en el codigo de Barra")

class activofijoch_subcategoria(models.Model):
    _name = "activofijosv.subcategoria"

    name = fields.Char(string="Subcategoria",required=True,help="Nombre de subcategoria")
    categoria_id = fields.Many2one("activofijosv.categoria",string="Categoria",required=True)
    prefijosubcategoria = fields.Char(string="Prefijo Activo Fijo",size=2, required=True,help="Codigo de 2 Digitos que representa la Subcategoria en el codigo de Barra")

class activofijoch_ubicacion(models.Model):
    _name = "activofijosv.ubicacion"

    name = fields.Char(string="Ubicacion",required=True,help="Ubicacion del Activo Fijo, sucursal")
    prefijoubicacion = fields.Char(string="Prefijo Activo Fijo", required=True,size=2,
                                      help="Codigo de 2 Digitos que representa la Ubicacion o sucursal en el codigo de Barra")

    # AGREGANDO CAMPO A LA TABLA COMPANIA HERENCIA
class res_company(models.Model):
    _inherit = "res.company"

    prefijocompany = fields.Char(string="*Prefijo Activo Fijo", required=True, size=2,
                                     help="Codigo de 2 Digitos que representa la Empresa en el codigo de Barra",default="A")
    # activofijo_id = fields.One2many("activofijosv.activo", "empresa_id", string="Activos fijos")

    #AGREGANDO CAMPO A LA TABLA DEPARTAMENTOS HERENCIA

class hr_department(models.Model):
    _inherit = "hr.department"

    prefijodepto = fields.Char(string="*Prefijo Activo Fijo", required=True,size=2,
                                      help="Codigo de 2 Digitos que representa Departamento o Area en el codigo de Barra")


class activofijosv_usados(models.Model):
    _name="activofijosv.usados"

    name = fields.Char(string="Anos",required=True,help="Anos de antiguedad del bien Comprado")
    porcentaje=fields.Float(string="Depreciacion %",help="Porcentaje de depreciacion del bien usado")



#from odoo import models, fields, api

# class activofijosv(models.Model):
#     _name = 'activofijosv.activofijosv'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

