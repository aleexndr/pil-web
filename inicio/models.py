from django.db import models


class Datos(models.Model):
    appat = models.CharField(db_column='apPat', max_length=255, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    apmat = models.CharField(db_column='apMat', max_length=255, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    nombres = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    usuario = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    contrasena = models.CharField(max_length=225, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datos'