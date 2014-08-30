SELECT 
  loc.id, loc.created, loc.modified, loc.active, loc.name, loc.slug, loc.uuid, loc.content_type_id as ctid, loc.point,  
  place.url, place.address, place.website, place.local_phone_number, place.international_phone_number, place.reference, place.types, 
  place.vicinity, place.location_ptr_id as pid, place.rating, 
  ct.id, ct.name, ct.app_label, ct.model
FROM 
  mtlocation_location as loc
  inner join django_content_type as ct on (loc.content_type_id = ct.id)
  left outer join public.mtlocation_gplace as place on  ( loc.id = place.location_ptr_id )
where
  ct.model not in ('transitstop')




SELECT *
FROM 
  mtlocation_location as loc
  inner join django_content_type as ct on (loc.content_type_id = ct.id)
  left outer join public.mtlocation_gplace as place on  ( loc.id = place.location_ptr_id )
where
  ct.model not in ('transitstop')


  