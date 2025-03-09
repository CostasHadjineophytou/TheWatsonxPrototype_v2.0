from typing import List, Dict, Any
from backend.services.service_checker import ServiceCheckerService
from .base_manager import BaseManager

class ServiceCheckerManager(BaseManager):
    """Business logic for checking service availability"""
    
    def __init__(self, service_checker: ServiceCheckerService):
        super().__init__()
        self.service_checker = service_checker
        
    def get_services(self) -> List[Dict[str, Any]]:
        """
        Get list of services with formatted information
        
        Returns:
            List of service dictionaries with formatted information
        """
        try:
            raw_services = self.service_checker.list_services()
            
            # Format services for display
            formatted_services = []
            for service in raw_services:
                formatted_service = {
                    'id': service.get('guid', 'Unknown'),
                    'name': service.get('name', 'Unnamed Service'),
                    'type': service.get('resource_plan_name', 'Unknown Type'),
                    'region': service.get('region_id', 'Unknown Region'),
                    'status': service.get('state', 'Unknown Status'),
                    'created_at': service.get('created_at', 'Unknown'),
                    'dashboard_url': service.get('dashboard_url', ''),
                    'resource_group': service.get('resource_group_name', 'Default'),
                    'raw_data': service  # Keep raw data for reference
                }
                formatted_services.append(formatted_service)
                
            return formatted_services
            
        except Exception as e:
            error = self.handle_business_error(
                message="Failed to fetch services",
                code="SERVICE_FETCH_ERROR",
                details={"error": str(e)}
            )
            return [{
                'id': 'ERROR',
                'name': 'Error',
                'type': 'Unknown',
                'region': 'Unknown',
                'status': 'Error',
                'error': error.message
            }]
            
    def get_service_details(self, service_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific service
        
        Args:
            service_id: ID of the service to retrieve
            
        Returns:
            Dictionary with service details
        """
        try:
            service_details = self.service_checker.get_service_details(service_id)
            
            # Get credentials for this service
            credentials = self.get_service_credentials(service_id)
            
            # Format service details
            formatted_details = {
                'id': service_details.get('guid', 'Unknown'),
                'name': service_details.get('name', 'Unnamed Service'),
                'type': service_details.get('resource_plan_name', 'Unknown Type'),
                'region': service_details.get('region_id', 'Unknown Region'),
                'status': service_details.get('state', 'Unknown Status'),
                'created_at': service_details.get('created_at', 'Unknown'),
                'dashboard_url': service_details.get('dashboard_url', ''),
                'resource_group': service_details.get('resource_group_name', 'Default'),
                'credentials': credentials,
                'raw_data': service_details  # Keep raw data for reference
            }
            
            return formatted_details
            
        except Exception as e:
            error = self.handle_unknown_error(e, "Failed to get service details")
            return {
                'id': 'ERROR',
                'name': 'Error',
                'type': 'Unknown',
                'error': error.message
            }
            
    def get_service_credentials(self, service_id: str = None) -> List[Dict[str, Any]]:
        """
        Get credentials for services
        
        Args:
            service_id: Optional service ID to filter credentials
            
        Returns:
            List of credential dictionaries
        """
        try:
            raw_keys = self.service_checker.list_resource_keys(service_id)
            
            # Format credentials
            formatted_keys = []
            for key in raw_keys:
                formatted_key = {
                    'id': key.get('guid', 'Unknown'),
                    'name': key.get('name', 'Unnamed Key'),
                    'created_at': key.get('created_at', 'Unknown'),
                    'status': key.get('state', 'Unknown'),
                    'service_id': key.get('resource_instance_id', ''),
                    'credentials': key.get('credentials', {})
                }
                formatted_keys.append(formatted_key)
                
            return formatted_keys
            
        except Exception as e:
            error = self.handle_unknown_error(e, "Failed to get service credentials")
            return [{
                'id': 'ERROR',
                'name': 'Error',
                'error': error.message
            }]
            
    def analyze_service_status(self) -> Dict[str, Any]:
        """
        Analyze the status of all services
        
        Returns:
            Dictionary with service status analysis
        """
        try:
            services = self.get_services()
            
            # Count services by type
            service_types = {}
            for service in services:
                service_type = service.get('type')
                if service_type not in service_types:
                    service_types[service_type] = 0
                service_types[service_type] += 1
                
            # Count services by status
            status_counts = {}
            for service in services:
                status = service.get('status')
                if status not in status_counts:
                    status_counts[status] = 0
                status_counts[status] += 1
                
            # Count services by region
            region_counts = {}
            for service in services:
                region = service.get('region')
                if region not in region_counts:
                    region_counts[region] = 0
                region_counts[region] += 1
                
            return {
                'total_services': len(services),
                'service_types': service_types,
                'status_counts': status_counts,
                'region_counts': region_counts,
                'services': services
            }
            
        except Exception as e:
            error = self.handle_unknown_error(e, "Failed to analyze service status")
            return {
                'error': error.message,
                'total_services': 0,
                'service_types': {},
                'status_counts': {},
                'region_counts': {},
                'services': []
            } 