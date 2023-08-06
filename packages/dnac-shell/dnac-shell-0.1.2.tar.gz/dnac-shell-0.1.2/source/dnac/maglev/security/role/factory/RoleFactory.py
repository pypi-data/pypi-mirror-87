from dnac.maglev.security.role.Role import Role
from dnac.maglev.security.role.ResourceType import ResourceType

# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class RoleFactory:
		
	# Create roles with variable number of resource types
	#
	@staticmethod
	def makeCustomRole( name, description,  *restypecontrols ):
		'''
			Factory (static) method to assemble a collection of resource types and create a custom role
		'''
	
		role_skeleton = '''
		{"role":"roleName","description":"Some description","resourceTypes":[{"type":"Assurance","operations":["gRead"]},{"type":"Assurance.Monitoring and Troubleshooting","operations":["gRead"]},{"type":"Assurance.Monitoring Settings","operations":["gRead"]},{"type":"Assurance.Troubleshooting Tools","operations":["gRead"]},{"type":"Network Design.Advanced Network Settings","operations":["gRead"]},{"type":"Network Design.Image Repository","operations":["gRead"]},{"type":"Network Design.Network Hierarchy","operations":["gRead","gCreate","gUpdate","gRemove"]},{"type":"Network Design.Network Profiles","operations":["gRead"]},{"type":"Network Design.Network Settings","operations":["gRead"]},{"type":"Network Design.Network Telemetry","operations":["gRead"]},{"type":"Network Design.Virtual Network","operations":["gRead"]},{"type":"Network Provision","operations":["gRead"]},{"type":"Network Provision.Image Update","operations":["gRead"]},{"type":"Network Provision.Inventory Management","operations":["gRead"]},{"type":"Network Provision.License","operations":["gRead"]},{"type":"Network Provision.PnP","operations":["gRead"]},{"type":"Network Provision.Provision","operations":["gRead"]},{"type":"Utilities.Scheduler","operations":["gRead"]},{"type":"Network Services","operations":["gRead"]},{"type":"Network Services.App Hosting","operations":["gRead"]},{"type":"Network Services.Bonjour","operations":["gRead"]},{"type":"Network Services.Cloud Connect","operations":["gRead"]},{"type":"Network Services.Stealthwatch","operations":["gRead"]},{"type":"Network Services.Umbrella","operations":["gRead"]},{"type":"Security","operations":["gRead"]},{"type":"Security.Group-Based Policy","operations":["gRead"]},{"type":"Security.IP Based Access Control","operations":["gRead"]},{"type":"Security.Security Advisories","operations":["gRead"]},{"type":"System.Basic","operations":["gRead","gCreate","gUpdate","gRemove"]},{"type":"System.Machine Reasoning","operations":["gRead"]},{"type":"System.System Management","operations":["gRead"]},{"type":"Utilities","operations":["gRead"]},{"type":"Utilities.Audit Log","operations":["gRead"]},{"type":"Utilities.Network Reasoner","operations":["gRead"]},{"type":"Utilities.Report","operations":["gRead"]},{"type":"Utilities.Search","operations":["gRead"]}]}
		'''


		if not isinstance(name, str) or not name or not len(name):
			raise ValueError('Invaid name for role specified - ignored')

		rt_list = []
		for resource_type_control in restypecontrols:
			resource_name, resource_controls = resource_type_control
			next_rt = ResourceType(resource_name, resource_controls)
			rt_list.append(next_rt)

		#
		# Form a skeleton role from skeleton JSon
		#
		role = Role.parseJson(role_skeleton)

		# Fill in the specified values
		#
		role.role = name
		role.description  = description 
		role.type  = 'CUSTOM'
		role.resourceTypes.extend(rt_list)

		return role
