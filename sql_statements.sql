UPDATE public.percelen
SET lat_middle=ST_X(ST_Centroid(lambert)); 
UPDATE public.percelen
SET lon_middle=ST_Y(ST_Centroid(lambert));

UPDATE public.percelen
SET lambert=ST_AsText(geom)

sha256(cast(lat_middle as text)||" "||cast(lon_middle as text))::bytea)

sha256(((((lat_middle)::text)::bytea || '\x'::bytea) || ((lon_middle)::text)::bytea))

ST_GeoHash(ST_SetSRID(ST_MakePoint(lat_middle,lon_middle),31370))

#delete alles behalve de eerste 100 records
DELETE FROM public.percelen
WHERE percelen.gid NOT IN (SELECT percelen.gid FROM public.percelen ORDER BY percelen.gid LIMIT 100);


#converteer coords van ene systeem naar het andere
UPDATE public.percelen
SET shp_wgs=ST_Transform(ST_GeomFromText(lambert,31370),4326);

#md5
UPDATE public.percelen
SET wgs_md5=md5(((((lat_middle)::text)::bytea || '\x'::bytea) || ((lon_middle)::text)::bytea));


UPDATE public.short_percelen
SET wgs_md5_bigint=CAST(md5(((((lat_middle)::text)::bytea || '\x'::bytea) || ((lon_middle)::text)::bytea)) as int);

#remove all records but keep the skeleton
DELETE FROM table_name;

