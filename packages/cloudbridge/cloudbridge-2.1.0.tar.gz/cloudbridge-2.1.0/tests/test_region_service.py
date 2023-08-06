import six

from cloudbridge.interfaces import Region

from tests import helpers
from tests.helpers import ProviderTestBase
from tests.helpers import standard_interface_tests as sit


class CloudRegionServiceTestCase(ProviderTestBase):

    _multiprocess_can_split_ = True

    @helpers.skipIfNoService(['compute.regions'])
    def test_storage_services_event_pattern(self):
        # pylint:disable=protected-access
        self.assertEqual(
            self.provider.compute.regions._service_event_pattern,
            "provider.compute.regions",
            "Event pattern for {} service should be '{}', "
            "but found '{}'.".format("regions",
                                     "provider.compute.regions",
                                     self.provider.compute.regions.
                                     _service_event_pattern))

    @helpers.skipIfNoService(['compute.regions'])
    def test_get_and_list_regions(self):
        regions = list(self.provider.compute.regions)
        sit.check_standard_behaviour(
            self, self.provider.compute.regions, regions[-1])

        for region in regions:
            self.assertIsInstance(
                region,
                Region,
                "regions.list() should return a cloudbridge Region")
            self.assertTrue(
                region.name,
                "Region name should be a non-empty string")

    @helpers.skipIfNoService(['compute.regions'])
    def test_regions_unique(self):
        regions = self.provider.compute.regions.list()
        unique_regions = set([region.id for region in regions])
        self.assertTrue(len(regions) == len(list(unique_regions)))

    @helpers.skipIfNoService(['compute.regions'])
    def test_current_region(self):
        current_region = self.provider.compute.regions.current
        self.assertIsInstance(current_region, Region)
        self.assertTrue(current_region in self.provider.compute.regions)

    @helpers.skipIfNoService(['compute.regions'])
    def test_zones(self):
        zone_find_count = 0
        test_zone = helpers.get_provider_test_data(self.provider, "placement")
        for region in self.provider.compute.regions:
            self.assertTrue(region.name)
            for zone in region.zones:
                self.assertTrue(zone.id)
                self.assertTrue(zone.name)
                self.assertTrue(zone.region_name is None or
                                isinstance(zone.region_name,
                                           six.string_types))
                if test_zone == zone.name:
                    zone_find_count += 1
        # zone info cannot be repeated between regions
        self.assertEqual(zone_find_count, 1)
