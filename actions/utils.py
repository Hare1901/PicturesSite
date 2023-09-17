from .models import Action

# Функция юыстрого доступа для созданиия новой активности
def create_action(user, verb, target=None):
 action = Action(user=user, verb=verb, target=target)
 action.save()