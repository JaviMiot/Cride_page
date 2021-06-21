import csv

listTemplate = ['name',
                'slug_name',
                'is_public',
                'verified',
                'members_limit'
                ]


def fillData(file, model):
    """Funtion to fill circle models with

    Args:
        file (str): path of csv file
        model (class model): model to add data
    """
    with open(file, newline='') as f:
        read = csv.DictReader(f, fieldnames=listTemplate)


        for row in read:

            if row['name'] != 'name':
                circle = model.objects.create(
                    name=row['name'],
                    slug_name=row['slug_name'],
                    is_public=bool(int(row['is_public'])),
                    verified=bool(int(row['verified'])),
                    members_limit=int(row['members_limit'])
                )

                circle.save()
