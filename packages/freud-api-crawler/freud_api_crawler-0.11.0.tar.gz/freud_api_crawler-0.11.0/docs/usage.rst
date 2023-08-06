=====
Usage
=====

Download Manifestations for specific Werk
--------

To use Freud API Crawler in a project::

    from freud_api_crawler.freud_api_crawler import *

    # the ID of the Work to download
    werk_id = "9d035a03-28d7-4013-adaf-63337d78ece4"

    # this path will be created/overriden
    out_dir='/home/csae8092/Desktop/data/freud_data/'

    # create a FrdWerk instance
    werk_obj = FrdWerk(werk_id=werk_id)

    # fetch all related manifestations
    rel_manifestations = werk_obj.manifestations

    # iterate over all manifestations, and save the fetched data as TEI
    for x in rel_manifestations:
      frd_man = FrdManifestation(
        out_dir=out_dir,
        manifestation_id=x['man_id']
      )
      frd_man.make_xml(save=True, limit=False)
