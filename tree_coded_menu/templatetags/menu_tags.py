from django import template
from django.db.models import Prefetch

from tree_coded_menu.models import MenuItem

register = template.Library()


@register.inclusion_tag("menu/menu.html", takes_context=True)
def draw_menu(context, menu_name):
    """Рисует древовидное меню с раскрытием активных элементов."""
    current_url = context["request"].path

    # Загружаем корневые пункты меню с prefetch для подменю
    menu_items = MenuItem.objects.filter(menu_name=menu_name, parent__isnull=True).prefetch_related(
        Prefetch("children", queryset=MenuItem.objects.all())
    )

    def mark_active_items(items):
        """Рекурсивно помечает активные элементы меню и раскрывает вложенные уровни."""
        found_active = False  # Флаг для отслеживания, найден ли активный элемент
        for item in items:
            item.active = current_url.startswith(item.get_url())
            if item.active:
                found_active = True
                item.expand = True  # Раскрываем этот элемент
            if item.children.exists():
                # Проверяем детей на активность
                child_active = mark_active_items(item.children.all())
                if child_active:
                    item.expand = True  # Если активен любой потомок, раскрываем родителя
                    found_active = True
        return found_active

    mark_active_items(menu_items)

    return {"menu_items": menu_items}
