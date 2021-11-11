from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import DictionaryObject, DecodedStreamObject, NameObject, createStringObject, ArrayObject
from odoo import models, fields, api, _
import io
import base64


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _post_pdf(self, save_in_attachment, pdf_content=None, res_ids=None):
        res = super(IrActionsReport, self)._post_pdf(save_in_attachment,
                                                     pdf_content=pdf_content,
                                                     res_ids=res_ids)

        if self.report_type == 'qweb-pdf' and self.model == 'account.move' and res_ids and len(
                res_ids) == 1 and self.id in self.env.company.sudo(
                ).sh_inv_merge_pdf_report_ids.ids:
            record = self.env[self.model].browse(res_ids)
            if record and record.sh_inv_merge_pdf_attachment_ids:
                writer = PdfFileWriter()
                pdf_content = [res]
                for attachment in record.sh_inv_merge_pdf_attachment_ids:
                    datas = base64.b64decode(
                        attachment.with_context(bin_size=False).datas)
                    pdf_content.append(datas)
                for document in pdf_content:
                    reader = PdfFileReader(io.BytesIO(document), strict=False)
                    for page in range(0, reader.getNumPages()):
                        writer.addPage(reader.getPage(page))
                with io.BytesIO() as _buffer:
                    writer.write(_buffer)
                    merged_pdf = _buffer.getvalue()
                    _buffer.close()
                    return merged_pdf
        return res