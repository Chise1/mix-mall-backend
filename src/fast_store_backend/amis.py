from typing import Optional

from fast_tmp.amis.formitem import FormItem
from fast_tmp.amis.forms import Form


class SubForm(FormItem):
    """
    InputSubForm 子表单
    https://aisuda.bce.baidu.com/amis/zh-CN/components/form/input-sub-form
    """

    type = "input-sub-form"
    multiple: Optional[bool]  # 是否为多选模式
    btnLabel: Optional[str]  # 按钮默认名称
    minLength: Optional[int]  # 限制最小个数。
    maxLength: Optional[int]  # 限制最大个数。
    draggable: Optional[bool]  # 是否可拖拽排序
    addable: Optional[bool]  # 是否可新增
    removable: Optional[bool]  # 是否可删除
    form: Form
    addButtonText: Optional[str]  # 自定义新增一项的文本
    showErrorMsg: Optional[bool]  # 是否在左下角显示报错信息
