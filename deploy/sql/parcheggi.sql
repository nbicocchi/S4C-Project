PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE parcheggi (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    comune TEXT NOT NULL,
    capienza INTEGER NOT NULL,
    attivo BOOLEAN NOT NULL,
    latitudine REAL NOT NULL,
    longitudine REAL NOT NULL
);
INSERT INTO parcheggi VALUES(0,'Parcheggio viale XVI Aprile','Castel San Pietro Terme',115,1,44.3951300000000017,11.5879499999999993);
INSERT INTO parcheggi VALUES(1,'Parcheggio dell''ospedale','Castel San Pietro Terme',40,1,44.3985839999999996,11.5933200000000002);
INSERT INTO parcheggi VALUES(2,'Parcheggio cimitero Castel San Pietro Terme','Castel San Pietro Terme',55,1,44.3928760000000011,11.5851830000000006);
INSERT INTO parcheggi VALUES(3,'Parcheggio piazza Tien An Men','Castel San Pietro Terme',22,1,44.3932169999999999,11.5798900000000006);
INSERT INTO parcheggi VALUES(4,'Parcheggio lungo Sillaro','Castel San Pietro Terme',25,1,44.3911200000000008,11.5888360000000005);
INSERT INTO parcheggi VALUES(5,'Parcheggio camper','Castel San Pietro Terme',13,1,44.3977689999999967,11.5931999999999995);
INSERT INTO parcheggi VALUES(6,'Parcheggio','Castel San Pietro Terme',300,1,44.3979560000000006,11.591882);
INSERT INTO parcheggi VALUES(7,'Parcheggio Gratuito','Castel San Pietro Terme',30,1,44.3915480000000002,11.5857220000000005);
INSERT INTO parcheggi VALUES(8,'Parcheggio','Castel San Pietro Terme',100,1,44.3942019999999999,11.5958590000000008);
INSERT INTO parcheggi VALUES(9,'Parcheggio','Castel San Pietro Terme',45,1,44.4011160000000018,11.5936079999999996);
INSERT INTO parcheggi VALUES(10,'Parcheggio','Castel San Pietro Terme',30,1,44.3995299999999986,11.5763850000000001);
INSERT INTO parcheggi VALUES(11,'Parcheggio','Castel San Pietro Terme',42,1,44.3903850000000019,11.5875699999999994);
INSERT INTO parcheggi VALUES(12,'Parcheggio Toscanella Piazza Gramsci','Dozza',53,1,44.3837505539670971,11.6360968731589995);
INSERT INTO parcheggi VALUES(13,'Parcheggio gratuito Imola','Imola',352,1,44.3531499999999994,11.70425);
INSERT INTO parcheggi VALUES(14,'Parcheggio Autostazione Imola','Imola',169,1,44.3576300000000003,11.7160899999999994);
INSERT INTO parcheggi VALUES(15,'Parcheggio Cavina Imola','Imola',34,1,44.3510399999999975,11.7114999999999991);
INSERT INTO parcheggi VALUES(16,'Parcheggio gratuito Zoo Acquario Imola','Imola',161,1,44.3588999999999984,11.7129899999999995);
INSERT INTO parcheggi VALUES(17,'Parcheggio piscina comunale','Imola',44,1,44.3887860000000031,11.5864449999999994);
INSERT INTO parcheggi VALUES(18,'Parcheggio Centro Città','Imola',266,1,44.3578371290955999,11.7132885085281994);
INSERT INTO parcheggi VALUES(19,'Parcheggio di piazzale ragazzi del ''99','Imola',112,1,44.3506080000000011,11.7115089999999995);
INSERT INTO parcheggi VALUES(20,'Parcheggio Scoperto','Imola',55,1,44.3464808971786013,11.7157076730678006);
INSERT INTO parcheggi VALUES(21,'Parcheggio in Via Serraglio','Imola',50,1,44.3591399999999964,11.7203800000000004);
INSERT INTO parcheggi VALUES(22,'Parcheggio mercato ortofrutticolo','Imola',212,1,44.3513599999999996,11.7105999999999994);
INSERT INTO parcheggi VALUES(23,'Parcheggio Dozza','Dozza',55,1,44.3599519999999998,11.6327700000000007);
INSERT INTO parcheggi VALUES(24,'Bus parking Dozza','Dozza',97,1,44.3588700000000031,11.6242999999999998);
COMMIT;
