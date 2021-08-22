from odoo import api, fields, models, _
import ast

class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product Brands'
    _rec_name = 'name'

    image_brand = fields.Image("Brand Image", max_width=1920, max_height=1920)
    name = fields.Text(string='Brand Name', required=True)
    description = fields.Text(string='Brand Name')
    sequence = fields.Integer(string='Sequence', help='Sequence can also be (de)prioritized in tree view')
    count = fields.Integer(string="Product Count", compute='_compute_product_count')
    products = fields.Many2one(string="Products")
    product_ids = fields.Many2many('product.template', 'brand_id',
                                   domain="[('id', 'not in', product_ids), ('brand_id', 'in', (False, None))]")
    record_ids = fields.Text(string='Records')

    @api.onchange('product_ids')
    def _compute_product_count(self):
        for record in self:
            record.count = len(record.product_ids)

            for product in record.product_ids._origin:
                if not product.brand_id._origin:
                    product._origin.brand_id = record._origin.id

            # x = MyList(1, 2, 3, 4)
            # y = MyList(2, 5, 2)
            # z = x - y
            if record.record_ids not in (False, None):
                a = ast.literal_eval(record.record_ids)
                b = record.product_ids
                c = list(set(a) - set(b._origin.ids))
                if len(c) > 0:
                    unlinked_ids = self.env['product.template'].sudo().browse(c)
                    for unlinked in unlinked_ids:
                        unlinked.brand_id = False
            if len(record.product_ids) > 0:
                record.record_ids = record.product_ids._origin.ids
            print('record_ids: ', record.record_ids)
            print('record: ',record)
            print('rec', record._context)

    # def unlink(self):
    #     # self.mapped('account_ids').unlink()
    #     print('self', self)
    #     return super(ProductBrand, self).unlink()

# ondelete="cascade"
class ProductTemplateInherited(models.Model):
    _inherit = 'product.template'

    brand_id = fields.Many2one("product.brand", string="Product Brand", ondelete="set null")

    @api.onchange('brand_id')
    def brand_id_onchange_product_ids(self):
        for rec in self:
            if rec.brand_id == False:
                raise Warning(_('This can only be unset by unlinking product under brand.'))

class ProductProduct(models.Model):
    _inherit = 'product.product'

    brand_id = fields.Many2one(related='product_tmpl_id.brand_id')

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):

        if self._context.get('search_default_brand_id'):
            print('search', self._context)
            print('search: ', self._context.get('search_default_brand_id'))
            args.append((('brand_id', 'child_of', self._context['search_default_brand_id'])))
        return super(ProductProduct, self)._search(args, offset=offset, limit=limit, order=order, count=count,
                                                   access_rights_uid=access_rights_uid)

class MyList(list):
    def __init__(self, *args):
        super(MyList, self).__init__(args)

    def __sub__(self, other):
        return self.__class__(*[item for item in self if item not in other])