from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.http import urlquote
import search as s
import zone as z
import json


def search(request):
    phrases = []
    i = 0
    query = 'q_' + str(i)
    while query in request.GET:
        phrase = request.GET.get(query, '').strip()
        if phrase:
            phrases.append(phrase)
        i += 1
        query = 'q_' + str(i)
    parties = []
    parties_str = request.GET.get('p', '')
    zone = int(request.GET.get('z', '0'))
    if parties_str:
        parties = [int(p) for p in parties_str.split(',')]
    return render(request, 'appelec/search.html', {'query': query,
                                                   'phrases': phrases,
                                                   'parties_js': json.dumps(parties),
                                                   'zone': zone,
                                                   'zones': z.zones,
                                                   'zones_js': json.dumps(z.zones),
                                                   'programs_js': json.dumps(z.programs)})


def autocomplete(request):
    query = request.GET.get('q', '')
    return JsonResponse({'results': ""})


def programs(request):
    phrases = []
    hits = {}
    i = 0
    query = 'q_' + str(i)
    while query in request.GET:
        phrase = request.GET.get(query, '').strip()
        if phrase:
            phrases.append(phrase)
        i += 1
        query = 'q_' + str(i)
    zone_str = request.GET.get('z', '0')
    parties_str = request.GET.get('p', '')
    parties = []
    zone = int(zone_str)
    if parties_str:
        parties = [int(p) for p in parties_str.split(',')]
    programs = z.intersec_zone_parties(zone, parties)
    if phrases:
        hits = s.programs(phrases, programs)
        if hits['hits']:
            for i in hits['hits']:
                i['pages'] = s.pages(phrases, i['_id'])
        else:
            return redirect(reverse('search') + '?' + request.META['QUERY_STRING'], permanent=False)
    query_string = '?z=' + zone_str + '&p=' + urlquote(parties_str)
    return render(request, 'appelec/programs.html', {'hits': hits,
                                                     'query_string': query_string,
                                                     'phrases': phrases})


def page(request, page):
    phrases = []
    i = 0
    query = 'q_' + str(i)
    while query in request.GET:
        phrase = request.GET.get(query, '').strip()
        if phrase:
            phrases.append(phrase)
        i += 1
        query = 'q_' + str(i)
    if phrases:
        content = s.page_highlight(phrases, page)
        html = content['highlight']['content'][0]
    else:
        content = s.page(page)
        html = content
    return HttpResponse(html)
