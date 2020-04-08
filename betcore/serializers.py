# betcore serializer
from .models import Category,League,Team,Bet,Outcome,Mybet,GenerateBetcode
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    # serializer for the category model

    leagues=serializers.HyperlinkedRelatedField(many=True,view_name='league-detail',read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'url',
            'name',
            'description',
            'created_at',
            'leagues'
            ]



class TeamSerializer(serializers.HyperlinkedModelSerializer):
    # serializer for the teams model
    class Meta:
        model = Team
        fields = [
            'id',
            'url',
            'name',
            'description',
            'league'
            ]

class LeagueSerializer(serializers.HyperlinkedModelSerializer):
    # serializer for the leagues model
    teams=TeamSerializer(many=True,read_only=True,)
    class Meta:
        model = League
        fields = [
            'id',
            'url',
            'name',
            'description',
            'category',
            'teams',
            ]

class OutcomeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    #this allows us to be able to edit the bet
    class Meta:
        model = Outcome
        fields = [
            'id',
            'bet',
            'option',
            'odd',
            'is_match_outcome'
        ]
        read_only_fields = ('bet',)
        #this allows us to makerefrence to a bet and not mess things up...check the doocs

class BetSerializer(serializers.HyperlinkedModelSerializer):
    home_team=serializers.SlugRelatedField(queryset=Team.objects.all(),slug_field='name')
    away_team=serializers.SlugRelatedField(queryset=Team.objects.all(),slug_field='name')
    outcomes = OutcomeSerializer(many=True)

    class Meta:
        model=Bet
        fields=[
            'id',
            'url',
            'match_time',
            'home_team',
            'away_team',
            'is_currently_playing',
            'is_available_for_betting',
            'outcomes'
        ]


    def create(self, validated_data):
        outcomes = validated_data.pop('outcomes')
        bet = Bet.objects.create(**validated_data)
        for outcome in outcomes:
            Outcome.objects.create(**outcome, bet=bet)
        return bet


class MyBetSerializer(serializers.ModelSerializer):
    bets =  BetSerializer(many=True,read_only=True)
    outcomes = OutcomeSerializer(many=True)

    class Meta:
        ordering = ['-id']
        model = Mybet
        fields=('id','bets','stake','total_return','customer_id','is_won','outcomes')
        extra_kwargs = {'outcomes':  {'required':False}}

# def create(self, instance, validated_data):
#         bets = validated_data.pop('bets')
#         selected_outcomes = []
#         total_odds = 0
#         if bets is not None:
#             for bet in bets:
#                 outcomes = bet.pop('outcomes', None)
#                 if outcomes is not None:
#                     for outcome in outcomes:
#                          if "id" in outcome.keys():
#                              real_outcome  = Outcome.objects.get(id=outcome["id"])
#                              if real_outcome.is_match_outcome == True:
#                                 c = Bet.objects.get(id=outcome["id"])

#                              else:
#                                 continue
#                         else:
#                                 selected_outcomes.append(c.id)




class BetcodeGeneratorSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ['-id']
        model = GenerateBetcode
        fields=('id','bets','stake','total_return','bet_code')
        extra_kwargs = {'bets': {'required': False}}
