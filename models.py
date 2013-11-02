
import peewee

DB_FILE = "database.db"
dbh = peewee.SqliteDatabase(DB_FILE)


class BaseModel(peewee.Model):

    class Meta:
        database = dbh

    @classmethod
    def all(cls):
        return list(cls.select())


class Owner(BaseModel):
    """ The web user who is also owner of the Organization
    """

    USER = 0
    ADMIN = 1
    ROOT = 2
    GROUPS = ((USER, u"user"), (ADMIN, u"admin"), (ROOT, u"superuser"))

    username = peewee.CharField(max_length=30, verbose_name=("Nom d'utilisateur"),
                                unique=True)
    password = peewee.CharField(max_length=150)
    phone = peewee.CharField(max_length=30, blank=True, null=True,
                             verbose_name=("Telephone"))
    group = peewee.CharField(choices=GROUPS, default=USER)
    isactive = peewee.BooleanField(default=True)
    islog = peewee.BooleanField(default=False)
    # is_admin = peewee.BooleanField()
    # is_active = peewee.BooleanField()
    # last_login = peewee.DateTimeField()
    # login_count = peewee.IntegerField()

    # def save(self):
    #     self.password = hashlib.sha224(self.password).hexdigest()
    #     super(Owner, self).save()

    def __unicode__(self):
        return u"{}".format(self.username)

    def full_mane(self):
        return u"{name} {group} {phone}".format(name=self.username,
                                                group=self.group,
                                                phone=self.phone)

