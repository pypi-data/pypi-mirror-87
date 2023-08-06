# -*- encoding: utf-8 -*-

"""Dependencies for usecases."""
from dependencies import Injector

from p360_contact_manager import common
from p360_contact_manager.api import brreg, p360
from p360_contact_manager.usecases.brreg_syncronize import BrregSyncronize
from p360_contact_manager.usecases.cache import CacheEnterprises
from p360_contact_manager.usecases.duplicates import Duplicates
from p360_contact_manager.usecases.ping import Ping
from p360_contact_manager.usecases.synchronize import Synchronize
from p360_contact_manager.usecases.update import Update

CommonScope = Injector.let(
    post=common.PostRequest,
    read=common.ReadLocalFile,
    write=common.WriteLocalFile,
)

GetAllEnterprisesScope = Injector.let(
    get_all_enterprises=p360.GetAllEnterprises,
    get_enterprises=p360.GetEnterprises,
    post=common.PostRequest,
)

GetAllCachedEnterprisesScope = Injector.let(
    get_all_enterprises=p360.GetAllCachedEnterprises,
    read=common.ReadLocalFile,
)

PingScope = Injector.let(
    run=Ping,
    post=common.PostRequest,
    ping_p360=p360.Ping,
)

CacheEnterprisesScope = GetAllEnterprisesScope.let(
    run=CacheEnterprises,
    write=common.WriteLocalFile,
)

DuplicatesScope = GetAllEnterprisesScope.let(
    run=Duplicates,
    write=common.WriteLocalFile,
)

UpdateScope = Injector.let(
    run=Update,
    update_enterprise=p360.UpdateEnterprise,
    post=common.PostRequest,
    read=common.ReadLocalFile,
    write=common.WriteLocalFile,
)

BrregSynchronizeScope = Injector.let(
    run=BrregSyncronize,
    get_country=common.GetCountryCode,
    get_all_organizations=brreg.GetAllOrganizations,
    get_organizations=brreg.GetOrganizations,
    get=common.GetRequest,
    write=common.WriteLocalFile,
)

SynchronizeScope = Injector.let(
    run=Synchronize,
    synchronize_enterprise=p360.SynchronizeEnterprise,
    post=common.PostRequest,
    read=common.ReadLocalFile,
    write=common.WriteLocalFile,
)


injected_functions = {
    'test': PingScope,
    'brreg_synchronize': BrregSynchronizeScope,
    'synchronize': SynchronizeScope,
    'cache_enterprises': CacheEnterprisesScope,
    'duplicates': DuplicatesScope,
    'update': UpdateScope,
}
