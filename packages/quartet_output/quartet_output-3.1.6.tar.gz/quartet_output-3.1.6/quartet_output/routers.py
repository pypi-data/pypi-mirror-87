# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2018 SerialLab Corp.  All rights reserved.

from rest_framework.routers import DefaultRouter
from quartet_output import viewsets

router = DefaultRouter()

router.register(
    r'end-points',
    viewsets.EndPointViewSet,
    basename='end-points'
)
router.register(
    r'authentication-info',
    viewsets.AuthenticationInfoViewSet,
    basename='authentication-info'
)
router.register(
    r'epcis-output-criteria',
    viewsets.EPCISOutputCriteriaViewSet,
    basename='epcis-output-criteria'
)
router.register(
    r'read-only-epcis-output-criteria',
    viewsets.ReadOnlyCriteriaViewSet,
    basename='read-only-epcis-output-criteria'
)

urlpatterns = router.urls
