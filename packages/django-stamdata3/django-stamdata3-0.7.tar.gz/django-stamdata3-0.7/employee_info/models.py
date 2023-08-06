from django.db import models


class Company(models.Model):
    companyCode = models.CharField('firma', max_length=2)

    def __str__(self):
        return self.companyCode

    class Meta:
        verbose_name = 'firma'
        verbose_name_plural = 'firmaer'


class Resource(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='firma', related_name='resource')
    resourceId = models.IntegerField('ressursnummer')
    firstName = models.CharField('fornavn', max_length=200)
    lastName = models.CharField('etternavn', max_length=200)
    socialSecurityNumber = models.CharField('fødselsnummer', max_length=11)
    status = models.CharField(max_length=1)

    def manages_list(self):
        users = []
        for user in self.manages.all():
            users.append(user)
        return users

    def subordinates(self):
        employees = []
        for organisation in self.manages.all():
            for employment in organisation.employments.all():
                employees.append(employment.resource)
        return employees

    def main_position(self, assume: bool = False):
        """
        Get the resources main position
        :type assume: bool Assume that the main position is the one with the
        highest percentage if main position is not specified
        :rtype: Employment
        """
        employments = self.employments.filter(mainPosition=True).first()
        if not employments:
            if assume:
                employments = self.employments.order_by('percentage')
                return employments.last()
        else:
            return employments

    def __str__(self):
        return '%s %s' % (self.firstName, self.lastName)

    class Meta:
        verbose_name = 'ansatt'
        verbose_name_plural = 'ansatte'
        unique_together = ['company', 'resourceId']


class CostCenter(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='firma', related_name='cost_centers')
    value = models.CharField('verdi', max_length=4)
    description = models.CharField('beskrivelse', max_length=200, blank=True, null=True)

    def __str__(self):
        return '%s %s (%s)' % (self.value, self.description, self.company.companyCode)

    class Meta:
        verbose_name = 'ansvar'
        verbose_name_plural = 'ansvar'
        unique_together = ['company', 'value']


class WorkPlace(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='firma', related_name='work_places')
    value = models.CharField('verdi', max_length=4)
    description = models.CharField('beskrivelse', max_length=200)

    def __str__(self):
        return '%s %s (%s)' % (self.value, self.description, self.company.companyCode)

    class Meta:
        verbose_name = 'arbeidssted'
        verbose_name_plural = 'arbeidssteder'
        unique_together = ['company', 'value']


class Function(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='firma', related_name='functions')
    value = models.CharField('verdi', max_length=4)
    description = models.CharField('beskrivelse', max_length=200)

    def __str__(self):
        return '%s %s (%s)' % (self.value, self.description, self.company.companyCode)

    class Meta:
        verbose_name = 'funksjon'
        verbose_name_plural = 'funksjoner'
        unique_together = ['company', 'value']


class Organisation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='firma', related_name='organisation')
    name = models.CharField('navn', max_length=200)
    orgId = models.CharField('nummer', max_length=6)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='overordnet', related_name='children',
                               null=True)
    manager = models.ForeignKey(Resource, on_delete=models.SET_NULL, verbose_name='leder', related_name='manages',
                                null=True)
    status = models.CharField(max_length=1)

    def __str__(self):
        return '%s %s' % (self.orgId, self.name)

    class Meta:
        verbose_name = 'organisasjonsenhet'
        verbose_name_plural = 'organisasjonsenheter'
        unique_together = ['company', 'orgId']


class Employment(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, verbose_name='ansatt', related_name='employments')
    employmentType = models.CharField(max_length=1)
    employmentTypeDescription = models.CharField('ansettelsestype', max_length=200)
    mainPosition = models.BooleanField('primært stillingsforhold')
    percentage = models.FloatField('prosent')
    postId = models.IntegerField()
    postIdDescription = models.CharField(max_length=200)
    postCode = models.IntegerField('stillingskode')
    postCodeDescription = models.CharField(max_length=200)

    dateFrom = models.DateField('dato fra')
    dateTo = models.DateField('dato til')

    costCenter = models.ForeignKey(CostCenter, on_delete=models.PROTECT, null=True, verbose_name='ansvar', related_name='employments')
    workPlace = models.ForeignKey(WorkPlace, on_delete=models.PROTECT, null=True, verbose_name='arbeidssted', related_name='employments')
    function = models.ForeignKey(Function, on_delete=models.PROTECT, null=True, verbose_name='funksjon', related_name='employments')
    organisation = models.ForeignKey(Organisation, on_delete=models.PROTECT, null=True,
                                     verbose_name='organisasjonsenhet', related_name='employments')

    def __str__(self):
        return '%s: %s' % (self.organisation, self.resource)

    class Meta:
        verbose_name = 'stillingsforhold'
        verbose_name_plural = 'stillingsforhold'
