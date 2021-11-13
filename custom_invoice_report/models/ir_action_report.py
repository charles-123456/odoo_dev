from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import DictionaryObject, DecodedStreamObject, NameObject, createStringObject, ArrayObject
from odoo import models, fields, api, _
import io
import base64


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _post_pdf(self, save_in_attachment, pdf_content=None, res_ids=None):
        # print('save in attachment',save_in_attachment)
        res = super(IrActionsReport, self)._post_pdf(save_in_attachment,
                                                     pdf_content=pdf_content,
                                                     res_ids=res_ids)
        if self.report_type == 'qweb-pdf' and self.model == 'account.move' and res_ids and len(
                res_ids) == 1 and self.id in self.env.company.sudo(
                ).sh_inv_merge_pdf_report_ids.ids:
            account_id = self.env['account.move'].search([('company_id.sh_inv_merge_pdf_report_ids','in',self.ids)],limit=1).id
            res_ids = [account_id]
            record = self.env['account.move'].browse(res_ids)
            # print('record',record)
            # print('rs ids',res_ids)
            writer = PdfFileWriter()
            pdf_content = [res]
            # print('pdf len',len(pdf_content))
            if record and record.account_pf_ids:
                # print('pf called',record)
                for attachment in record.account_pf_ids:
                    # print('pf attach called',attachment)
                    first = base64.b64decode(
                        attachment.with_context(bin_size=False).pf_doc)
                    pdf_content.append(first)
            if record and record.account_esi_ids :
                # print('second called', record)
                for attachment in record.account_esi_ids :
                    second = base64.b64decode(
                        attachment.with_context(bin_size=False).esi_doc)
                    pdf_content.append(second)
            if record and record.account_pt_ids :
                # print('thired called', record)
                for attachment in record.account_pt_ids :
                    thired = base64.b64decode(
                        attachment.with_context(bin_size=False).pt_doc)
                    pdf_content.append(thired)
            if record and record.account_tds_ids :
                # print('fifth called', record)
                for attachment in record.account_tds_ids :
                    fourth = base64.b64decode(
                        attachment.with_context(bin_size=False).tds_doc)
                    pdf_content.append(fourth)
            if record and record.inv_insurance_ids :
                # print('fourth called', record)
                for attachment in record.inv_insurance_ids :
                    fifth = base64.b64decode(
                        attachment.with_context(bin_size=False).insurance_doc)
                    pdf_content.append(fifth)
            for document in pdf_content :
                # print('document', document)
                reader = PdfFileReader(io.BytesIO(document), strict=False)
                for page in range(0, reader.getNumPages()) :
                    # print('pages',page)
                    writer.addPage(reader.getPage(page))
            with io.BytesIO() as _buffer :
                writer.write(_buffer)
                merged_pdf = _buffer.getvalue()
                _buffer.close()
                return merged_pdf
        return res
