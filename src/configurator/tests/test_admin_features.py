from django.test import TestCase

from src.configurator.admin import ConfigOptionAdminForm, FeatureListField
from src.configurator.models import ConfigOption


class FeatureListFieldTests(TestCase):
    def test_lines_become_a_list(self):
        field = FeatureListField()
        self.assertEqual(field.clean('Панорамні вікна\n\nТераса'), ['Панорамні вікна', 'Тераса'])
        self.assertEqual(field.clean(''), [])
        self.assertEqual(field.prepare_value(['A', 'B']), 'A\nB')

    def test_admin_form_roundtrip(self):
        option = ConfigOption.objects.create(
            option_type=ConfigOption.OptionType.TIER,
            code='prime',
            name='Prime',
            features=['Утеплення', 'Вікно'],
        )
        form = ConfigOptionAdminForm(instance=option)
        self.assertEqual(form['features'].value(), 'Утеплення\nВікно')

        data = {
            name: '' if form[name].value() is None else form[name].value()
            for name in form.fields
        }
        data['features'] = 'Опалення\nТераса'
        bound = ConfigOptionAdminForm(data=data, instance=option)
        self.assertTrue(bound.is_valid(), bound.errors)
        saved = bound.save()
        self.assertEqual(saved.features, ['Опалення', 'Тераса'])
