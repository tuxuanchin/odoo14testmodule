from odoo import api, fields, models, _
from io import BytesIO
from xlsxwriter.workbook import Workbook
from datetime import datetime
import base64


class OrderReportWizard(models.TransientModel):
    _name = "order.report.wizard"
    _description = "Print Order Wizard"

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")

    def action_print_excel_report(self):
        # Cau hinh file Excel
        buf = BytesIO()
        wb = Workbook(buf)
        ws = wb.add_worksheet('Báo cáo KQKD')
        wb.formats[0].font_name = 'Times New Roman'
        wb.formats[0].font_size = 12
        ws.set_paper(9)
        ws.set_margins(left=0.28, right=0.28, top=0.5, bottom=0.5)
        ws.fit_to_pages(1, 0)  # -- 1 page wide and as long as necessary.
        ws.set_landscape()

        # Dinh dang header
        table_header = wb.add_format({
            'bold': 1, 'text_wrap': 1, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_name': 'Times New Roman', 'bg_color': '#faf602'
        })
        # Dinh dang cac dong trong table
        format_text = wb.add_format({
            'bold': 1, 'text_wrap': 1, 'align': 'center', 'valign': 'vcenter', 'border': 1,
            'font_name': 'Times New Roman'
        })
        format_number = wb.add_format({
            'bold': 1, 'text_wrap': 1, 'align': 'right', 'valign': 'vcenter', 'border': 1,
            'font_name': 'Times New Roman'
        })

        query = f"""
                SELECT name, amount_untaxed, amount_discount, amount_total
                FROM sale_order
                WHERE state = 'sale'
                    AND create_date BETWEEN '{self.date_from}' and '{self.date_to}'
                ORDER BY amount_total
                     """
        self.env.cr.execute(query)
        orders = self.env.cr.fetchall()

        # Set kich thuoc cot
        ws.set_column('A:A', 15)
        ws.set_column('B:B', 15)
        ws.set_column('C:C', 15)
        ws.set_column('D:D', 15)

        # Header
        ws.write("A{row}".format(row=1), "Ma Hoa Don", table_header)
        ws.write("B{row}".format(row=1), "Tong Tien", table_header)
        ws.write("C{row}".format(row=1), "Giam Gia", table_header)
        ws.write("D{row}".format(row=1), "Tong Phai Tra", table_header)

        # In du lieu cac dong
        row_expense = 1
        total_amount_untaxed = 0
        total_discount = 0
        total_amount = 0
        for order in orders:
            row_expense += 1
            total_amount_untaxed += order[1]
            total_amount += order[3]

            ws.write("A{row}".format(row=row_expense), order[0], format_text)
            ws.write("B{row}".format(row=row_expense), order[1], format_number)

            # Check nếu order nào ko có khuyến mại, type sẽ là NONE, ko format được.
            if not order[2]:
                ws.write("C{row}".format(row=row_expense), "0", format_number)
                total_discount += 0
            else:
                ws.write("C{row}".format(row=row_expense), round(order[2], 2), format_number)
                total_discount += order[2]
            ws.write("D{row}".format(row=row_expense), order[3], format_number)

        # Dong cuoi cung
        ws.write("A{row}".format(row=row_expense+1), "TOTAL", table_header)
        ws.write("B{row}".format(row=row_expense+1), round(total_amount_untaxed, 2), format_number)
        ws.write("C{row}".format(row=row_expense+1), round(total_discount, 2), format_number)
        ws.write("D{row}".format(row=row_expense+1), round(total_amount, 2), format_number)

        wb.close()
        buf.seek(0)
        xlsx_data = buf.getvalue()
        report_name = "THEO DOI DON HANG.xlsx"
        vals = {
            'name': report_name,
            'datas': base64.b64encode(xlsx_data),
            'store_fname': report_name,
            'type': 'binary',
            'res_model': self._name,
            'res_id': self.id,
        }
        file_xls = self.env['ir.attachment'].create(vals)

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/' + str(file_xls.id) + '?download=true',
            'target': 'new',
        }
