from django.db import models
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _


class Organization(models.Model):
    """

    机构，多法人结构，有多个用户和多个管理员
    """
    name = models.CharField(max_length=128, unique=True, verbose_name=_("Name"))
    logo = models.ImageField(upload_to="logo", null=True, verbose_name=_('Logo'))
    users = models.ManyToManyField('users.User', related_name='orgs', blank=True)
    admins = models.ManyToManyField('users.User', related_name='admin_orgs', blank=True)
    created_by = models.IntegerField(null=True, blank=True, verbose_name=_("Created By"))
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_("Created Date"))
    description = models.TextField(max_length=128, default='', blank=True, verbose_name=_('description'))

    CACHE_PREFIX = 'DEVOPS_ORG_{}'
    ROOT_ID_NAME = '-1'
    DEFAULT_ID_NAME = '0'

    class Meta:
        verbose_name = _("Organization")

    def __str__(self):
        return self.name

    def set_to_cache(self):
        key_id = self.CACHE_PREFIX.format(self.id)
        key_name = self.CACHE_PREFIX.format(self.name)
        cache.set(key_id, self, 3600)
        cache.set(key_name, self, 3600)

    def expire_cache(self):
        key_id = self.CACHE_PREFIX.format(self.id)
        key_name = self.CACHE_PREFIX.format(self.name)
        cache.delete(key_id)
        cache.delete(key_name)

    @classmethod
    def get_instance_from_cache(cls, oid):
        key = cls.CACHE_PREFIX.format(oid)
        return cache.get(key, None)

    @classmethod
    def get_instance(cls, id_or_name, default=True):
        cached = cls.get_instance_from_cache(id_or_name)
        if cached:
            return cached

        if not id_or_name:
            return cls.default() if default else None
        elif id_or_name == cls.DEFAULT_ID_NAME:
            return cls.default()
        elif id_or_name == cls.ROOT_ID_NAME:
            return cls.root()

        try:
            if str(id_or_name).isnumeric():
                org = cls.objects.get(id=id_or_name)
            else:
                org = cls.objects.get(name=id_or_name)
        except cls.DoesNotExist:
            org = cls.default() if default else None
        return org

    def get_org_users(self):
        users = self.users.all()
        return users

    def get_org_admins(self):
        return self.admins.all()

    def can_admin_by(self, user):
        if user.is_superuser:
            return True
        if user in list(self.get_org_admins()):
            return True
        return False

    @classmethod
    def get_user_admin_orgs(cls, user):
        admin_orgs = []
        if user.is_anonymous:
            return admin_orgs
        elif user.is_superuser:
            admin_orgs = list(cls.objects.all())
            admin_orgs.append(cls.default())
        elif user.is_org_admin:
            admin_orgs = user.admin_orgs.all()
        return admin_orgs

    """
    
    分超管和非超管
    """

    @classmethod
    def default(cls):
        return None

    @classmethod
    def root(cls):
        return cls(id=cls.ROOT_ID_NAME, name=cls.ROOT_ID_NAME)

    def is_root(self):
        if self.id is self.ROOT_ID_NAME:
            return True
        else:
            return False

    def is_default(self):
        if self.id is self.DEFAULT_ID_NAME:
            return True
        else:
            return False

    #: Use this method initial org
    @classmethod
    def initial(cls):
        organization = Organization(id=-1,
                                    name='虚拟机构',
                                    description='虚拟机构',
                                    logo='')
        organization.save()


class ProductRole(models.Model):
    PROJECT = "project"
    WIKI = "wiki"
    TEST = "test"
    TYPE_CHOICES = ((PROJECT, "Project"), (WIKI, "Wiki"), (TEST, "Test"))

    ADMIN = "Admin"
    MEMBER = "Member"
    ROLE_CHOICES = ((ADMIN, "Project"), (MEMBER, "Member"))

    user = models.ForeignKey("users.User", related_name="productroles", on_delete=models.CASCADE)
    product = models.CharField(choices=TYPE_CHOICES, max_length=32)
    role = models.CharField(choices=ROLE_CHOICES, max_length=32)

    class Meta:
        db_table = "productroles"
        verbose_name = _("Organization")
        # 唯一索引
        unique_together = ("user", "product")
