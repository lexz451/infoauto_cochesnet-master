from django.http import HttpResponse

def chrome_extension_update(request, *args, **kwargs):
    xml = """<?xml version='1.0' encoding='UTF-8'?>
    <gupdate xmlns='https://www.google.com/update2/response' protocol='2.0'>
      <app appid='{id}'>
        <updatecheck codebase='{url}' version='2.0' />
      </app>
    </gupdate>""".format(
        id="jahgclpohnbcokommijdgoefbmcebobm",
        url="https://smartmotorlead.net/static/resources/chrome_extension.crx"
    )

    return HttpResponse(xml, content_type='text/xml')
