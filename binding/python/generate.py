# This file is part of RBDyn.
#
# RBDyn is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RBDyn is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RBDyn.  If not, see <http://www.gnu.org/licenses/>.

from pybindgen import *
import sys



def import_sva_types(mod):
  mod.add_class('MotionVec', foreign_cpp_namespace='sva', import_from_module='spacevecalg')
  mod.add_class('ForceVec', foreign_cpp_namespace='sva', import_from_module='spacevecalg')
  mod.add_class('RBInertia', foreign_cpp_namespace='sva', import_from_module='spacevecalg')
  mod.add_class('ABInertia', foreign_cpp_namespace='sva', import_from_module='spacevecalg')
  mod.add_class('PTransform', foreign_cpp_namespace='sva', import_from_module='spacevecalg')



def import_eigen3_types(mod):
  mod.add_class('Vector3d', foreign_cpp_namespace='Eigen', import_from_module='eigen3')
  mod.add_class('Vector6d', foreign_cpp_namespace='Eigen', import_from_module='eigen3')

  mod.add_class('Matrix3d', foreign_cpp_namespace='Eigen', import_from_module='eigen3')
  mod.add_class('Matrix6d', foreign_cpp_namespace='Eigen', import_from_module='eigen3')

  mod.add_class('MatrixXd', foreign_cpp_namespace='Eigen', import_from_module='eigen3')
  mod.add_class('VectorXd', foreign_cpp_namespace='Eigen', import_from_module='eigen3')

  mod.add_class('Quaterniond', foreign_cpp_namespace='Eigen', import_from_module='eigen3')



def build_body(bd):
  bd.add_copy_constructor()
  bd.add_constructor([param('sva::RBInertia', 'rbInertia'),
                      param('int', 'id'),
                      param('std::string', 'name')])
  bd.add_constructor([param('double', 'mass'),
                      param('Eigen::Vector3d', 'com'),
                      param('Eigen::Matrix3d', 'inertia'),
                      param('int', 'id'),
                      param('std::string', 'name')])

  bd.add_method('id', retval('int'), [], is_const=True)
  bd.add_method('name', retval('std::string'), [], is_const=True)
  bd.add_method('inertia', retval('sva::RBInertia'), [], is_const=True)

  bd.add_binary_comparison_operator('==')
  bd.add_binary_comparison_operator('!=')

  bd.add_output_stream_operator()



def build_joint(jt):
  jt.add_enum('Type', ['RevX', 'RevY', 'RevZ',
                       'PrismX', 'PrismY', 'PrismZ',
                       'Spherical', 'Free', 'Fixed'])

  jt.add_copy_constructor()
  jt.add_constructor([param('rbd::Joint::Type', 'type'), param('bool', 'forward'),
                      param('int', 'id'), param('std::string', 'name')])

  jt.add_method('type', retval('rbd::Joint::Type'), [], is_const=True)

  jt.add_method('direction', retval('double'), [], is_const=True)
  jt.add_method('forward', retval('bool'), [], is_const=True)
  jt.add_method('forward', None, [param('double', 'forward')])

  jt.add_method('params', retval('int'), [], is_const=True)
  jt.add_method('dof', retval('int'), [], is_const=True)
  jt.add_method('id', retval('int'), [], is_const=True)
  jt.add_method('name', retval('std::string'), [], is_const=True)

  jt.add_method('motionSubspace', retval('Eigen::MatrixXd'), [], is_const=True)

  jt.add_method('sPose', retval('sva::PTransform'),
                [param('const std::vector<double>&', 'q')],
                throw=[dom_ex], custom_name='pose')

  jt.add_method('sMotion', retval('sva::MotionVec'),
                [param('const std::vector<double>&', 'alpha')],
                throw=[dom_ex], custom_name='motion')


  jt.add_binary_comparison_operator('==')
  jt.add_binary_comparison_operator('!=')

  jt.add_output_stream_operator()



def build_mbg(mbg):
  mbg.add_constructor([])

  mbg.add_method('addBody', None, [param('rbd::Body', 'body')], throw=[dom_ex])
  mbg.add_method('addJoint', None, [param('rbd::Joint', 'joint')], throw=[dom_ex])

  mbg.add_method('linkBodies', None,
                 [param('int', 'b1Id'), param('sva::PTransform', 'tB1'),
                  param('int', 'b2Id'), param('sva::PTransform', 'tB2'),
                  param('int', 'jointId'), param('bool', 'isB1toB2', default_value='true')],
                 throw=[out_ex])

  mbg.add_method('nrNodes', retval('int'), [], is_const=True)
  mbg.add_method('nrJoints', retval('int'), [], is_const=True)

  mbg.add_method('makeMultiBody', retval('rbd::MultiBody'),
                 [param('int', 'rootById'), param('bool', 'isFixed')])



def build_mb(mb):
  mb.add_constructor([])

  mb.add_constructor([param('std::vector<rbd::Body>', 'bodies'),
                      param('std::vector<rbd::Joint>', 'joints'),
                      param('std::vector<int>', 'pred'),
                      param('std::vector<int>', 'succ'),
                      param('std::vector<int>', 'parent'),
                      param('std::vector<sva::PTransform>', 'Xt')])

  mb.add_copy_constructor()

  mb.add_method('nrBodies', retval('int'), [], is_const=True)
  mb.add_method('nrJoints', retval('int'), [], is_const=True)

  mb.add_method('nrParams', retval('int'), [], is_const=True)
  mb.add_method('nrDof', retval('int'), [], is_const=True)

  mb.add_method('bodies', retval('std::vector<rbd::Body>'), [], is_const=True)
  mb.add_method('sBody', retval('rbd::Body'), [param('int', 'num')],
                is_const=True, throw=[out_ex], custom_name='body')

  mb.add_method('joints', retval('std::vector<rbd::Joint>'), [], is_const=True)
  mb.add_method('sJoint', retval('rbd::Joint'), [param('int', 'num')],
                is_const=True, throw=[out_ex], custom_name='joint')

  mb.add_method('predecessors', retval('std::vector<int>'), [], is_const=True)
  mb.add_method('sPredecessor', retval('int'), [param('int', 'num')],
                is_const=True, throw=[out_ex], custom_name='predecessor')

  mb.add_method('successors', retval('std::vector<int>'), [], is_const=True)
  mb.add_method('sSuccessor', retval('int'), [param('int', 'num')],
                is_const=True, throw=[out_ex], custom_name='successor')

  mb.add_method('parents', retval('std::vector<int>'), [], is_const=True)
  mb.add_method('sParent', retval('int'), [param('int', 'num')],
                is_const=True, throw=[out_ex], custom_name='parent')

  mb.add_method('transforms', retval('std::vector<sva::PTransform>'), [], is_const=True)
  mb.add_method('sTransform', retval('sva::PTransform'), [param('int', 'num')],
                is_const=True, throw=[out_ex], custom_name='transform')

  mb.add_method('sBodyIndexById', retval('int'), [param('int', 'id')],
                is_const=True, throw=[out_ex], custom_name='bodyIndexById')

  mb.add_method('sJointIndexById', retval('int'), [param('int', 'id')],
                is_const=True, throw=[out_ex], custom_name='jointIndexById')



def build_mbc(mbc):
  mbc.add_constructor([])
  mbc.add_constructor([param('const rbd::MultiBody&', 'mb')])

  mbc.add_copy_constructor()

  mbc.add_instance_attribute('q', 'std::vector<std::vector<double> >')
  mbc.add_instance_attribute('alpha', 'std::vector<std::vector<double> >')
  mbc.add_instance_attribute('alphaD', 'std::vector<std::vector<double> >')

  mbc.add_instance_attribute('force', 'std::vector<sva::ForceVec>')

  mbc.add_instance_attribute('jointConfig', 'std::vector<sva::PTransform>')
  mbc.add_instance_attribute('jointVelocity', 'std::vector<sva::MotionVec>')
  mbc.add_instance_attribute('jointTorque', 'std::vector<std::vector<double> >')

  mbc.add_instance_attribute('motionSubspace', 'std::vector<Eigen::MatrixXd>',
                             getter='python_motionSubspace',
                             setter='python_motionSubspace')

  mbc.add_instance_attribute('bodyPosW', 'std::vector<sva::PTransform>')
  mbc.add_instance_attribute('parentToSon', 'std::vector<sva::PTransform>')

  mbc.add_instance_attribute('bodyVelW', 'std::vector<sva::MotionVec>')
  mbc.add_instance_attribute('bodyVelB', 'std::vector<sva::MotionVec>')
  mbc.add_instance_attribute('bodyAccB', 'std::vector<sva::MotionVec>')

  mbc.add_instance_attribute('gravity', 'Eigen::Vector3d')

def build_utility(mod):
  mod.add_function('sParamToVector', None,
                   [param('const std::vector<std::vector<double> >&', 'v'),
                    param('Eigen::VectorXd&', 'e')],
                   custom_name='paramToVector',
                   throw=[out_ex])

  mod.add_function('sVectorToParam', None,
                   [param('const Eigen::VectorXd&', 'e'),
                    param('std::vector<std::vector<double> >&', 'v')],
                   custom_name='vectorToParam',
                   throw=[out_ex])

def build_algo(mod):
  mod.add_function('sForwardKinematics', None,
                   [param('const MultiBody&', 'mb'),
                    param('MultiBodyConfig&', 'mbc')],
                   custom_name='forwardKinematics',
                   throw=[dom_ex])

  mod.add_function('sForwardVelocity', None,
                   [param('const MultiBody&', 'mb'),
                    param('MultiBodyConfig&', 'mbc')],
                   custom_name='forwardVelocity',
                   throw=[dom_ex])



def build_jacobian(jac):
  jac.add_constructor([])
  jac.add_constructor([param('const rbd::MultiBody&', 'mb'),
                       param('int', 'bodyId'),
                       param('const Eigen::Vector3d&', 'point',
                             default_value='Eigen::Vector3d::Zero()')],
                     throw=[out_ex])

  jac.add_method('sJacobian', retval('Eigen::MatrixXd'),
                 [param('const rbd::MultiBody&', 'mb'),
                  param('const rbd::MultiBodyConfig&', 'mbc')],
                 throw=[dom_ex], custom_name='jacobian')

  jac.add_method('sSubMultiBody', retval('rbd::MultiBody'),
                 [param('const rbd::MultiBody&', 'mb')],
                 throw=[dom_ex], custom_name='subMultiBody',
                 is_const=True)

  jac.add_method('jointsPath', retval('std::vector<int>'),
                 [], is_const=True)


def build_id(id):
  id.add_constructor([])
  id.add_constructor([param('const rbd::MultiBody&', 'mb')])


  id.add_method('sInverseDynamics', None,
                 [param('const rbd::MultiBody&', 'mb'),
                  param('rbd::MultiBodyConfig&', 'mbc')],
                 throw=[dom_ex], custom_name='inverseDynamics')


if __name__ == '__main__':
  if len(sys.argv) < 2:
    sys.exit(1)

  rbd = Module('_rbdyn', cpp_namespace='::rbd')
  rbd.add_include('<Body.h>')
  rbd.add_include('<Joint.h>')
  rbd.add_include('<MultiBody.h>')
  rbd.add_include('<MultiBodyConfig.h>')
  rbd.add_include('<MultiBodyGraph.h>')
  rbd.add_include('<FK.h>')
  rbd.add_include('<FV.h>')
  rbd.add_include('<Jacobian.h>')
  rbd.add_include('<ID.h>')

  dom_ex = rbd.add_exception('std::domain_error', foreign_cpp_namespace=' ',
                             message_rvalue='%(EXC)s.what()')
  out_ex = rbd.add_exception('std::out_of_range', foreign_cpp_namespace=' ',
                             message_rvalue='%(EXC)s.what()')

  # import Eigen3 and sva types
  import_eigen3_types(rbd)
  import_sva_types(rbd)

  body = rbd.add_class('Body')
  joint = rbd.add_class('Joint')
  mb = rbd.add_class('MultiBody')
  mbc = rbd.add_struct('MultiBodyConfig')
  mbg = rbd.add_class('MultiBodyGraph')
  jac = rbd.add_class('Jacobian')
  id = rbd.add_class('InverseDynamics')

  # build list type
  rbd.add_container('std::vector<double>', 'double', 'vector')
  rbd.add_container('std::vector<int>', 'int', 'vector')
  rbd.add_container('std::vector<std::vector<double> >', 'std::vector<double>', 'vector')
  rbd.add_container('std::vector<rbd::Body>', 'rbd::Body', 'vector')
  rbd.add_container('std::vector<rbd::Joint>', 'rbd::Joint', 'vector')
  rbd.add_container('std::vector<sva::PTransform>', 'sva::PTransform', 'vector')
  rbd.add_container('std::vector<sva::MotionVec>', 'sva::MotionVec', 'vector')
  rbd.add_container('std::vector<sva::ForceVec>', 'sva::ForceVec', 'vector')
  rbd.add_container('std::vector<Eigen::MatrixXd>', 'Eigen::MatrixXd', 'vector')

  build_body(body)
  build_joint(joint)
  build_mbg(mbg)
  build_mb(mb)
  build_mbc(mbc)
  build_jacobian(jac)
  build_id(id)

  build_utility(rbd)
  build_algo(rbd)

  with open(sys.argv[1], 'w') as f:
    rbd.generate(f)

