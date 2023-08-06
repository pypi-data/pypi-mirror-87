from unittest import TestCase
from k9.helm import *
from k9.core import set_default_namespace, delete_namespace
from k9.cluster_init import *

from k9.pretty_object import PrettyObject

po = PrettyObject()


class TestClusterInit(TestCase):

    def test_jenkins_ready(self):
        """

        """
        pass

    def test_jenkins_logs(self):
        """

        """
        pass

    def test_efk_ready(self):
        """

        """
        pass

    def test_efk_kibana_logs(self):
        """

        """
        pass

    def test_efk_elastic_logs(self):
        """

        """
        pass

    def test_sonarqube_ready(self):
        """

        """
        pass

    def test_sonarqube_logs(self):
        """

        """
        pass

    def test_prometheus_ready(self):
        """

        """
        pass

    def test_prometheus_logs(self):
        """

        """
        pass

    def test_grafana_ready(self):
        """

        """
        pass

    def test_grafana_logs(self):
        """

        """
        pass

    def test_cluster_init_full_np(self):
        """

        """
        pass

    def test_cluster_init_full_cicd(self):
        """

        """
        pass

    def test_jinja_xml(self):
        """

        """
        pass
