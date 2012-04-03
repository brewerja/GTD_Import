SELECT AddGeometryColumn('gtd', 'geom', 2163, 'POINT', 2);
UPDATE gtd SET geom = ST_Transform(ST_GeomFromText('POINT(' || lon || ' ' || lat || ')', 4326), 2163);
CREATE INDEX idx_locations_geom ON gtd USING gist(geom);

ALTER TABLE gtd ADD COLUMN geog geography(POINT, 4326);
UPDATE gtd SET geog = ST_GeogFromText('SRID=4326; POINT(' || lon || ' ' || lat || ')');
CREATE INDEX idx_locations_geog ON gtd USING gist(geog);

VACUUM ANALYZE gtd;
