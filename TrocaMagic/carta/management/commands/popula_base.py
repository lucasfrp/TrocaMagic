from django.core.management.base import BaseCommand
from carta import models
import json
from carta.models import NamesCard

class Command(BaseCommand):
    help ="Carrega a base em json para o bando de dados."
    
    def handle(self, *args, **options):
        
        def save_field(kwargs, cls, key_field, field_name=None, commit=True):
            def save(cls, key_field, field_name, data):
                try:
                    data = cls.objects.get(**{field_name:data})
                except cls.DoesNotExist:
                    data = cls(**{field_name:data})
                    data.save()
                return data
            
            if not kwargs.get(key_field,False):
                return
            if not field_name:
                field_name = key_field
            data = kwargs.pop(key_field)
            if type(data) == list:
                data = [save(cls, key_field, field_name, each) for each in data]
            else:
                data = save(cls, key_field, field_name, data)
                
            if commit:
                kwargs[key_field] = data
            return data
        
        json_data = open('carta/dados/AllSets.json')
        data = json.load(json_data)
        for titulo_expansao in data.keys():
            expansao = data[titulo_expansao]
            print '\n'
            print '***Adicionando %s***' % expansao['name'].encode(encoding='UTF-8', errors='strinct')
            cards = expansao.pop('cards')
            save_field(expansao, models.TypeSet, 'type')
            try:
                expansao = models.Set.objects.get(name=expansao['name'])
            except models.Set.DoesNotExist:
                expansao = models.Set(**expansao)
                expansao.save()
            for card in cards:
                try:
                    models.Card.objects.get(set=expansao, name=card['name'])
                    #print '%s - Ja existe na base.' % card['name'].encode(encoding='UTF-8', errors='strinct')
                except models.Card.DoesNotExist:
                    kwargs = card
                    save_field(kwargs, models.Layout, 'layout')   
                    save_field(kwargs, models.Rarity, 'rarity')
                    save_field(kwargs, models.Artist, 'artist')
                    colors = save_field(kwargs, models.Color, 'colors', 'color', commit=False)
                    subtypes = save_field(kwargs, models.Subtype, 'subtypes', 'subtype', commit=False)
                    supertypes = save_field(kwargs, models.Supertype, 'supertypes', 'supertype', commit=False)
                    names = kwargs.pop('names') if kwargs.get('names', False) else None
                    types = save_field(kwargs, models.Type, 'types', 'type', commit=False)
                                      
                    carta = models.Card(**kwargs)                
                    carta.set = expansao
                    carta.save()
                    if colors:
                        carta.colors.add(*colors)
                    if subtypes:
                        carta.subtypes.add(*subtypes)
                    if supertypes:
                        carta.supertypes.add(*supertypes)
                    if types:
                        carta.types.add(*types)
                    if names:
                        for name in names:
                            Nome = NamesCard(nome=name, carta=carta)
                            Nome.save()                            
                    #print '%s - Adicionado com sucesso.' % carta.name.encode(encoding='UTF-8', errors='strinct')    
            print '***%s adicionado com sucesso***' % expansao.name.encode(encoding='UTF-8', errors='strinct')
            print '\n' 
        json_data.close()