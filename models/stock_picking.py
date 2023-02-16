# -*- coding: utf-8 -*-

from odoo import fields, models,api
import xlwt
from xlwt import easyxf
from cStringIO import StringIO
import base64
import itertools
from operator import itemgetter
import operator


class StockPicking(models.Model):
    _inherit = "stock.picking"

    excel_file = fields.Binary('Excel Report')
    file_name = fields.Char('Excel File')
    



    @api.multi
    def export_stock_ledger(self):
        workbook = xlwt.Workbook()
        filename = 'Albaran.xls'
        # Style
        main_header_style = easyxf('font:height 400;pattern: pattern solid, fore_color gray25;'
                                   'align: horiz center;font: color black; font:bold True;'
                                   "borders: top thin,left thin,right thin,bottom thin")

        header_style = easyxf('font:height 200;pattern: pattern solid, fore_color gray25;'
                              'align: horiz center;font: color black; font:bold True;'
                              "borders: top thin,left thin,right thin,bottom thin")

        group_style = easyxf('font:height 200;pattern: pattern solid, fore_color gray25;'
                              'align: horiz left;font: color black; font:bold True;'
                              "borders: top thin,left thin,right thin,bottom thin")

        text_left = easyxf('font:height 150; align: horiz left;' "borders: top thin,bottom thin")
        text_right_bold = easyxf('font:height 200; align: horiz right;font:bold True;' "borders: top thin,bottom thin")
        text_right_bold1 = easyxf('font:height 200; align: horiz right;font:bold True;' "borders: top thin,bottom thin", num_format_str='0.00')
        text_center = easyxf('font:height 150; align: horiz center;' "borders: top thin,bottom thin")
        text_right = easyxf('font:height 150; align: horiz right;' "borders: top thin,bottom thin",
                            num_format_str='0.00')

        worksheet = []
        
        worksheet.append(1)
        work=0
        worksheet[work] = workbook.add_sheet("albaran")
        
        for i in range(0, 12):
            worksheet[work].col(i).width = 140 * 30

        worksheet[work].write(4, 0, 'Orden', header_style)
        worksheet[work].write(4, 1, 'Fecha', header_style)
        worksheet[work].write(4, 2, 'Origen', header_style)
        worksheet[work].write(4, 3, 'Destino', header_style)
        worksheet[work].write(4, 4, 'Movimiento', header_style)


        worksheet[work].write(5, 0, self.origin, text_center)
        worksheet[work].write(5, 1, self.min_date, text_center)
        worksheet[work].write(5, 2, self.location_id.name, text_center)
        worksheet[work].write(5, 3, self.location_dest_id.name,text_center)
        worksheet[work].write(5, 4, self.name, text_center)





        tags = ['Producto','Cantidad']

        r= 6
        
        c = 1
        for tag in tags:
            worksheet[work].write(r, c, tag, header_style)
            c+=1
            

       
        
        r=7
        
        for line in self.pack_operation_product_ids:
            
            c=1       
            worksheet[work].write(r, c, line.product_id.display_name, text_left)
            c+=1
            worksheet[work].write(r,c,line.qty_done, text_left)
           
           
            r+=1
           

        fp = StringIO()
        workbook.save(fp)
        export_id = self.write(
            {'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename})
        fp.close()

       


 
