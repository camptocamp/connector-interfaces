from odoo.addons.base.ir.ir_qweb.assetsbundle import WebAsset
from odoo.http import request
from odoo.tools import func
from datetime import datetime


def _patched_last_modified(self):
    # if we use `debug=assets` this check on `modified` is bypassed
    # It's even better because like this we can force reload of our resources
    # even w/out debug mode one.
    debug_modules = [
        x.strip() for x in request.params.get('debug_mods', '').split(',')
        if x.strip()
    ]
    if self._filename and debug_modules:
        print('DEBUGGING MODULES', debug_modules)
        to_reload = False
        for mod in debug_modules:
            if mod in self._filename:
                to_reload = True
                break
        if to_reload:
            print('FORCED RELOAD', self._filename)
            return datetime.now()
    return self.orig_last_modified


def patch_web_asset():
    WebAsset.orig_last_modified = WebAsset.last_modified
    WebAsset.last_modified = func.lazy_property(_patched_last_modified)
    print('PATCHED WebAsset to force resources reload')
