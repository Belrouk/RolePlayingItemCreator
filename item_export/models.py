from django.db import models
from copy import copy
# Create your models here.
from django.core.files.storage import FileSystemStorage
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table, PageBreak, TableStyle, Spacer, BaseDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse


class PDFExporter(object):
    """docstring for PDFExporter."""
    def __init__(self, *args, **kwargs):
        super(PDFExporter, self).__init__()
        self.rarity_to_color =  {
            '10' :  'black',
            '20' :  'lightgreen',
            '30' :  'lightblue',
            '40' :  'thistle',
            '50' :  'gold',
            '60' :  'orange',
        }

    def _gen_file_name(self, items):
        return "Magic_Item_Batch"

    def _get_styles(self):
        return None

    def _get_table_style(self, rarity):
        table_formatting = [
            ('BACKGROUND', (0,0), (0,0), colors.grey),
            ('BACKGROUND', (0,1), (0,1), colors.lightgrey),
            ('INNERGRID', (0,0), (2,2), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 1.5, colors.black),
            ]
        t = TableStyle(table_formatting)
        return t
    def _process_item(self, item, styleSheet=getSampleStyleSheet()):
        if item.attunement.lower() != "no":
            attunement = "Requires Attunement"
        else:
            attunement = ""
        if item.value is not None:
            value_text = " - "+item.value
        else:
            value_text = ""

        h1_style = copy(styleSheet["Heading1"])
        h1_style.fontName = 'Helvetica'
        h1_style.alignment = TA_CENTER
        h1_style.color = self.rarity_to_color[str(item.rarity)]

        title = Paragraph('''<para align=center color={0}><b>{1}</b><font size=10 color=black> - {2}</font></para>'''.format(self.rarity_to_color[str(item.rarity)],item.name, item.rarity_text),
                            h1_style)

        type = Paragraph('''<para align=center>{0} - {1}{2}</para>'''.format(item.type_text, attunement, value_text),
                          styleSheet["BodyText"])
        desc = Paragraph('''<para align=left> {0} </para>'''.format(item.description),
                          styleSheet["BodyText"])
        benefit = Paragraph('''<para align=left> {0} </para>'''.format(item.benefits),
                          styleSheet["BodyText"])
        return {
                'name': title,
                'type': type,
                #'rarity': item.rarity_text,
                'value': value_text,
                'desc': desc,
                'benefit': benefit,
                }




    def generate(self, items):
        file_name = self._gen_file_name(items)
        styleSheet = getSampleStyleSheet()

        doc =  SimpleDocTemplate("/tmp/"+file_name, pagesize=letter)
        # frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1')
        # frame2 = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height, id='col2')

        tables = []
        for item in items:
            item_data= self._process_item(item)
            table_data = [
                # ["00"],
                # ["01"],
                # ["02"],
                # ['03']
                [item_data['name']],
                [item_data['type']],
                [item_data['desc']],
                [item_data['benefit']]
                ]

            t=Table(table_data, colWidths=[4.5*inch] * 1 )
            t.setStyle(self._get_table_style(item.rarity))
            tables.append(t)
            tables.append(Spacer(1, 0.05*inch))

        elements = []
        available_height = doc.height
        for table in tables:
            table_height = table.wrap(0, available_height)[1]
            if available_height < table_height:
               elements.extend([PageBreak(), table])
               if table_height < doc.height:
                   available_height = doc.height - table_height
               else:
                   available_height = table_height % doc.height
            else:
               elements.append(table)
               available_height = available_height - table_height



        doc.build(elements)

        fs = FileSystemStorage("/tmp")
        with fs.open(file_name) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = (
                     'attachment; filename="{0}.pdf"'.format(file_name))
            return response
