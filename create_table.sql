-- Table: gtd

-- DROP TABLE gtd;

CREATE TABLE gtd
(
  id bigint NOT NULL,
  date date,
  approxdate character varying(100),
  extended boolean,
  resolution date,
  country integer,
  region integer,
  provstate character varying(100),
  city character varying(100),
  vicinity boolean,
  location text,
  summary text,
  crit1 boolean,
  crit2 boolean,
  crit3 boolean,
  doubtterr boolean,
  alternative integer,
  multiple boolean,
  conflict boolean,
  success boolean,
  suicide boolean,
  attacktype1 integer,
  attacktype2 integer,
  attacktype3 integer,
  targtype1 integer,
  corp1 character varying(200),
  target1 character varying(250),
  natlty1 integer,
  targtype2 integer,
  corp2 character varying(200),
  target2 character varying(200),
  natlty2 integer,
  targtype3 integer,
  corp3 character varying(200),
  target3 character varying(150),
  natlty3 integer,
  gname character varying(150),
  gsubname character varying(100),
  gname2 character varying(100),
  gsubname2 character varying(100),
  gname3 character varying(100),
  gsubname3 character varying(100),
  motive text,
  guncertain1 boolean,
  guncertain2 boolean,
  guncertain3 boolean,
  nperps integer,
  nperpcap integer,
  claimed boolean,
  claimmode integer,
  claimconf boolean,
  claim2 boolean,
  claimmode2 integer,
  claimconf2 boolean,
  claim3 boolean,
  claimmode3 integer,
  claimconf3 boolean,
  compclaim boolean,
  weaptype1 integer,
  weapsubtype1 integer,
  weaptype2 integer,
  weapsubtype2 integer,
  weaptype3 integer,
  weapsubtype3 integer,
  weaptype4 integer,
  weapsubtype4 integer,
  weapdetail character varying(800),
  nkill real,
  nkillus integer,
  nkillter integer,
  nwound integer,
  nwoundus integer,
  nwoundter integer,
  property boolean,
  propextent integer,
  propvalue bigint,
  propcomment character varying(1000),
  ishostkid boolean,
  nhostkid integer,
  nhostkidus integer,
  nhours integer,
  ndays integer,
  divert character varying(100),
  kidhijcountry character varying(100),
  ransom boolean,
  ransomamt integer,
  ransomamtus integer,
  ransompaid integer,
  ransompaidus integer,
  ransomnote text,
  hostkidoutcome integer,
  nreleased integer,
  addnotes text,
  scite1 character varying(500),
  scite2 character varying(500),
  scite3 character varying(500),
  dbsource character varying(100),
  CONSTRAINT gtd_pkey PRIMARY KEY (id),
  CONSTRAINT gtd_country_fkey FOREIGN KEY (country)
      REFERENCES countries (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_region_fkey FOREIGN KEY (region)
      REFERENCES regions (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_alternative_fkey FOREIGN KEY (alternative)
      REFERENCES alternatives (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_attacktype1_fkey FOREIGN KEY (attacktype1)
      REFERENCES attack_types (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_attacktype2_fkey FOREIGN KEY (attacktype2)
      REFERENCES attack_types (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_attacktype3_fkey FOREIGN KEY (attacktype3)
      REFERENCES attack_types (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_targtype1_fkey FOREIGN KEY (targtype1)
      REFERENCES target_types (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_natlty1_fkey FOREIGN KEY (natlty1)
      REFERENCES countries (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_targtype2_fkey FOREIGN KEY (targtype2)
      REFERENCES target_types (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_natlty2_fkey FOREIGN KEY (natlty2)
      REFERENCES countries (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_targtype3_fkey FOREIGN KEY (targtype3)
      REFERENCES target_types (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_natlty3_fkey FOREIGN KEY (natlty3)
      REFERENCES countries (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_claimmode_fkey FOREIGN KEY (claimmode)
      REFERENCES claim_modes (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_claimmode2_fkey FOREIGN KEY (claimmode2)
      REFERENCES claim_modes (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_claimmode3_fkey FOREIGN KEY (claimmode3)
      REFERENCES claim_modes (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_weaptype1_fkey FOREIGN KEY (weaptype1)
      REFERENCES weapon_types (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_weapsubtype1_fkey FOREIGN KEY (weapsubtype1)
      REFERENCES weapon_subtypes (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_weaptype2_fkey FOREIGN KEY (weaptype2)
      REFERENCES weapon_types (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_weapsubtype2_fkey FOREIGN KEY (weapsubtype2)
      REFERENCES weapon_subtypes (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_weaptype3_fkey FOREIGN KEY (weaptype3)
      REFERENCES weapon_types (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_weapsubtype3_fkey FOREIGN KEY (weapsubtype3)
      REFERENCES weapon_subtypes (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_weaptype4_fkey FOREIGN KEY (weaptype4)
      REFERENCES weapon_types (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_weapsubtype4_fkey FOREIGN KEY (weapsubtype4)
      REFERENCES weapon_subtypes (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_propextent_fkey FOREIGN KEY (propextent)
      REFERENCES damage (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT gtd_hostkidoutcome_fkey FOREIGN KEY (hostkidoutcome)
      REFERENCES hostage_outcomes (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE gtd
  OWNER TO username;
