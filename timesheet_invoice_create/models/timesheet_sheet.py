from odoo import models,fields,api,_
from odoo.exceptions import UserError

class TimesheetInherited(models.Model):
    _inherit ="hr_timesheet.sheet"



    def _merge_timesheet_tree_view(self):
        inv_obj = self.env['hr_timesheet.sheet'].browse(self._context.get('active_ids', []))
        print(inv_obj)
        all_obj = []
        for val in inv_obj:
            if val.user_id.id == self.user_id.id:
                all_obj.append(val)
                if len(all_obj) >1:
                    time = 0.0
                    sep_obj =[]
                    for  count, value in enumerate(all_obj):
                        timesheet = self.env['hr_timesheet.sheet'].search([('id','=',value)])
                        time += timesheet.total_time
                        if count == 0:
                            sep_obj.append(timesheet)
                        if count > 0:
                            timesheet.unlink()
                        final_obj = self.env['hr_timesheet.sheet'].search([('id','=',sep_obj[0])])
                        final_obj.write({'total_time':time})
                else:
                    raise UserError(_('Please Select Same User Records to Merge!!!'))