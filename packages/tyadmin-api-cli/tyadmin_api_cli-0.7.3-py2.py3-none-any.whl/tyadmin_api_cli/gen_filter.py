import os

from django.conf import settings
from django.db.models import DateTimeField, ForeignKey, ImageField, FileField

from tyadmin_api_cli.contants import MAIN_DISPLAY, SYS_LABELS
from tyadmin_api_cli.utils import init_django_env


def gen_filter(project_name_settings, user_label_list):
    init_django_env(project_name_settings)
    import django
    from django.conf import settings
    if not user_label_list:
        user_label_list = settings.TY_ADMIN_CONFIG["GEN_APPS"]
    model_list = []
    model_pic_dict = {}
    model_fk_dict = {}
    model_date_dict = {}
    app_model_import_dict = {}
    gen_labels = SYS_LABELS + user_label_list
    for one in django.apps.apps.get_models():
        columns = []
        model_name = one._meta.model.__name__
        model_ver_name = one._meta.verbose_name
        app_label = one._meta.app_label
        if app_label in gen_labels:
            try:
                app_model_import_dict[app_label].append(model_name)
            except KeyError:
                app_model_import_dict[app_label] = [model_name]
            img_field_list = []
            fk_field_list = []
            date_field_list = []
            for filed in one.objects.model._meta.fields:
                name = filed.name
                ver_name = filed.verbose_name
                if isinstance(filed, ImageField):
                    img_field_list.append('"' + name + '"')
                if isinstance(filed, FileField):
                    img_field_list.append('"' + name + '"')
                if isinstance(filed, ForeignKey):
                    help_text = filed.help_text.replace(MAIN_DISPLAY + "__", "")
                    fk_field_list.append(name + "$分割$" + help_text)
                if isinstance(filed, DateTimeField):
                    date_field_list.append(name)
                if filed.__class__.__name__ == "TimeZoneField":
                    img_field_list.append('"' + name + '"')
            model_pic_dict[model_name] = img_field_list
            model_fk_dict[model_name] = fk_field_list
            model_date_dict[model_name] = date_field_list
            model_list.append(model_name)
    filters_txt = f"""from django_filters import rest_framework as filters
from tyadmin_api.custom import DateFromToRangeFilter
$model_import占位$"""
    model_import_rows = []
    for app, m_list in app_model_import_dict.items():
        if app in ["auth", "contenttypes"]:
            txt = f'from django.contrib.{app}.models import {", ".join(m_list)}\n'
        else:
            txt = f'from {app}.models import {", ".join(m_list)}\n'
        model_import_rows.append(txt)
    model_import_rows = model_import_rows[:-1] + [model_import_rows[-1].replace("\n", "")]
    filters_txt = filters_txt.replace("$model_import占位$", "".join(model_import_rows))
    for (model, img_field_l), (model_2, fk_field_l), (model_3, date_field_l) in zip(model_pic_dict.items(), model_fk_dict.items(),
                                                                                    model_date_dict.items()):
        fk_display_p = []
        for one_fk in fk_field_l:
            fk_name, fk_text = one_fk.split("$分割$")
            fk_one_line = f'    {fk_name}_text = filters.CharFilter(field_name="{fk_name}")\n'
            fk_display_p.append(fk_one_line)
        date_range_p = []
        for one_date in date_field_l:
            date_one_line = f'    {one_date} = DateFromToRangeFilter(field_name="{one_date}")\n'
            date_range_p.append(date_one_line)
        filters_txt += f"""


class {model}Filter(filters.FilterSet):
{"".join(fk_display_p)}{"".join(date_range_p)}
    class Meta:
        model = {model}
        exclude = [{",".join(img_field_l)}]"""

    # if os.path.exists(f'{settings.BASE_DIR}/tyadmin_api/auto_filters.py'):
    #     print("已存在filters.py跳过")
    # else:
    with open(f'{settings.BASE_DIR}/tyadmin_api/auto_filters.py', 'w', encoding='utf-8') as fw:
        fw.write(filters_txt)


if __name__ == '__main__':
    name = input("请输入项目settings位置:")
    gen_filter(name, None)
