#ifndef OPENMESH_PYTHON_DECIMATER_HH
#define OPENMESH_PYTHON_DECIMATER_HH

#include "MeshTypes.hh"
#include <OpenMesh/Tools/Decimater/ModBaseT.hh>
#include <OpenMesh/Tools/Decimater/ModAspectRatioT.hh>
#include <OpenMesh/Tools/Decimater/ModEdgeLengthT.hh>
#include <OpenMesh/Tools/Decimater/ModHausdorffT.hh>
#include <OpenMesh/Tools/Decimater/ModIndependentSetsT.hh>
#include <OpenMesh/Tools/Decimater/ModNormalDeviationT.hh>
#include <OpenMesh/Tools/Decimater/ModNormalFlippingT.hh>
#include <OpenMesh/Tools/Decimater/ModProgMeshT.hh>
#include <OpenMesh/Tools/Decimater/ModQuadricT.hh>
#include <OpenMesh/Tools/Decimater/ModRoundnessT.hh>
#include <OpenMesh/Tools/Decimater/DecimaterT.hh>

#include <cstdio>

#include <pybind11/pybind11.h>

namespace py = pybind11;
namespace OM = OpenMesh;


template <class Handle>
void expose_module_handle(py::module& m, const char *_name) {
	py::class_<Handle>(m, _name)
		.def(py::init<>())
		.def("is_valid", &Handle::is_valid)
		;
}

template <class Module>
py::list infolist(Module& _self) {
	const typename Module::InfoList& infos = _self.infolist();
	py::list res;
	for (size_t i = 0; i < infos.size(); ++i) {
		res.append(infos[i]);
	}
	return res;
}

template <class Mesh>
void copy_locked_vertex_prop(Mesh& _mesh, const std::string& _name) {
	if (!_mesh.template py_has_property<OM::VertexHandle>(_name)) {
		const std::string msg = "Vertex property \"" + _name + "\" does not exist.";
		PyErr_SetString(PyExc_RuntimeError, msg.c_str());
		throw py::error_already_set();
	}
	for (auto vh : _mesh.vertices()) {
		const auto val = _mesh.template py_property<OM::VertexHandle, typename Mesh::VPropHandle>(_name, vh);
		// BaseDecimaterT ctor requests vertex status
		_mesh.status(vh).set_locked(py::cast<bool>(val));
	}
}

template <class Mesh>
void copy_feature_vertex_prop(Mesh& _mesh, const std::string& _name) {
	if (!_mesh.template py_has_property<OM::VertexHandle>(_name)) {
		const std::string msg = "Vertex property \"" + _name + "\" does not exist.";
		PyErr_SetString(PyExc_RuntimeError, msg.c_str());
		throw py::error_already_set();
	}
	for (auto vh : _mesh.vertices()) {
		const auto val = _mesh.template py_property<OM::VertexHandle, typename Mesh::VPropHandle>(_name, vh);
		// BaseDecimaterT ctor requests vertex status
		_mesh.status(vh).set_feature(py::cast<bool>(val));
	}
}

template <class Mesh>
void copy_feature_edge_prop(Mesh& _mesh, const std::string& _name) {
	if (!_mesh.template py_has_property<OM::EdgeHandle>(_name)) {
		const std::string msg = "Edge property \"" + _name + "\" does not exist.";
		PyErr_SetString(PyExc_RuntimeError, msg.c_str());
		throw py::error_already_set();
	}
	for (auto eh : _mesh.edges()) {
		const auto val = _mesh.template py_property<OM::EdgeHandle, typename Mesh::EPropHandle>(_name, eh);
		// BaseDecimaterT ctor requests edge status
		_mesh.status(eh).set_feature(py::cast<bool>(val));
	}
}

template <class Mesh>
void copy_status_props(Mesh& _mesh,
                       py::object _locked_vertex_propname,
                       py::object _feature_vertex_propname,
                       py::object _feature_edge_propname)
{
	if (!_locked_vertex_propname.is_none())
		copy_locked_vertex_prop(_mesh, py::cast<std::string>(_locked_vertex_propname));
	if (!_feature_vertex_propname.is_none())
		copy_feature_vertex_prop(_mesh, py::cast<std::string>(_feature_vertex_propname));
	if (!_feature_edge_propname.is_none())
		copy_feature_edge_prop(_mesh, py::cast<std::string>(_feature_edge_propname));
}

template <class Mesh>
void expose_decimater(py::module& m, const char *_name) {

	typedef OM::Decimater::ModBaseT<Mesh> ModBase;
	typedef OM::Decimater::ModAspectRatioT<Mesh> ModAspectRatio;
	typedef OM::Decimater::ModEdgeLengthT<Mesh> ModEdgeLength;
	typedef OM::Decimater::ModHausdorffT<Mesh> ModHausdorff;
	typedef OM::Decimater::ModIndependentSetsT<Mesh> ModIndependentSets;
	typedef OM::Decimater::ModNormalDeviationT<Mesh> ModNormalDeviation;
	typedef OM::Decimater::ModNormalFlippingT<Mesh> ModNormalFlipping;
	typedef OM::Decimater::ModProgMeshT<Mesh> ModProgMesh;
	typedef OM::Decimater::ModQuadricT<Mesh> ModQuadric;
	typedef OM::Decimater::ModRoundnessT<Mesh> ModRoundness;

	typedef OM::Decimater::ModHandleT<ModAspectRatio> ModAspectRatioHandle;
	typedef OM::Decimater::ModHandleT<ModEdgeLength> ModEdgeLengthHandle;
	typedef OM::Decimater::ModHandleT<ModHausdorff> ModHausdorffHandle;
	typedef OM::Decimater::ModHandleT<ModIndependentSets> ModIndependentSetsHandle;
	typedef OM::Decimater::ModHandleT<ModNormalDeviation> ModNormalDeviationHandle;
	typedef OM::Decimater::ModHandleT<ModNormalFlipping> ModNormalFlippingHandle;
	typedef OM::Decimater::ModHandleT<ModProgMesh> ModProgMeshHandle;
	typedef OM::Decimater::ModHandleT<ModQuadric> ModQuadricHandle;
	typedef OM::Decimater::ModHandleT<ModRoundness> ModRoundnessHandle;

	typedef OM::Decimater::DecimaterT<Mesh> Decimater;
	typedef typename ModProgMesh::Info Info;

	// Decimater
	// ----------------------------------------

	char buffer[64];
	snprintf(buffer, sizeof buffer, "%s%s", _name, "Decimater");

	py::class_<Decimater>(m, buffer)
		.def(py::init<Mesh&>(), py::keep_alive<1,2>())

		.def("decimate", [](Decimater& _self,
		                    size_t _n_collapses,
		                    py::object _locked_vertex_propname,
		                    py::object _feature_vertex_propname,
		                    py::object _feature_edge_propname)
			{
				copy_status_props(_self.mesh(), _locked_vertex_propname,
				                  _feature_vertex_propname, _feature_edge_propname);
				_self.decimate(_n_collapses);
			},
			py::arg("n_collapses")=0,
			py::arg("locked_vertex_propname")=py::none(),
			py::arg("feature_vertex_propname")=py::none(),
			py::arg("feature_edge_propname")=py::none())

		.def("decimate_to", [](Decimater& _self,
		                       size_t _n_vertices,
		                       py::object _locked_vertex_propname,
		                       py::object _feature_vertex_propname,
		                       py::object _feature_edge_propname)
			{
				copy_status_props(_self.mesh(), _locked_vertex_propname,
				                  _feature_vertex_propname, _feature_edge_propname);
				_self.decimate_to(_n_vertices);
			},
			py::arg("n_vertices"),
			py::arg("locked_vertex_propname")=py::none(),
			py::arg("feature_vertex_propname")=py::none(),
			py::arg("feature_edge_propname")=py::none())

		.def("decimate_to_faces", [](Decimater& _self,
		                             size_t _n_vertices,
		                             size_t _n_faces,
		                             py::object _locked_vertex_propname,
		                             py::object _feature_vertex_propname,
		                             py::object _feature_edge_propname)
			{
				copy_status_props(_self.mesh(), _locked_vertex_propname,
				                  _feature_vertex_propname, _feature_edge_propname);
				_self.decimate_to_faces(_n_vertices, _n_faces);
			},
			py::arg("n_vertices")=0,
			py::arg("n_faces")=0,
			py::arg("locked_vertex_propname")=py::none(),
			py::arg("feature_vertex_propname")=py::none(),
			py::arg("feature_edge_propname")=py::none())

		.def("initialize", [](Decimater& _self) { return _self.initialize(); })
		.def("is_initialized", [](Decimater& _self) { return _self.is_initialized(); })

		.def("add", [](Decimater& _self, ModAspectRatioHandle& _mod) { return _self.add(_mod); })
		.def("add", [](Decimater& _self, ModEdgeLengthHandle& _mod) { return _self.add(_mod); })
		.def("add", [](Decimater& _self, ModHausdorffHandle& _mod) { return _self.add(_mod); })
		.def("add", [](Decimater& _self, ModIndependentSetsHandle& _mod) { return _self.add(_mod); })
		.def("add", [](Decimater& _self, ModNormalDeviationHandle& _mod) { return _self.add(_mod); })
		.def("add", [](Decimater& _self, ModNormalFlippingHandle& _mod) { return _self.add(_mod); })
		.def("add", [](Decimater& _self, ModProgMeshHandle& _mod) { return _self.add(_mod); })
		.def("add", [](Decimater& _self, ModQuadricHandle& _mod) { return _self.add(_mod); })
		.def("add", [](Decimater& _self, ModRoundnessHandle& _mod) { return _self.add(_mod); })

		.def("remove", [](Decimater& _self, ModAspectRatioHandle& _mod) { return _self.remove(_mod); })
		.def("remove", [](Decimater& _self, ModEdgeLengthHandle& _mod) { return _self.remove(_mod); })
		.def("remove", [](Decimater& _self, ModHausdorffHandle& _mod) { return _self.remove(_mod); })
		.def("remove", [](Decimater& _self, ModIndependentSetsHandle& _mod) { return _self.remove(_mod); })
		.def("remove", [](Decimater& _self, ModNormalDeviationHandle& _mod) { return _self.remove(_mod); })
		.def("remove", [](Decimater& _self, ModNormalFlippingHandle& _mod) { return _self.remove(_mod); })
		.def("remove", [](Decimater& _self, ModProgMeshHandle& _mod) { return _self.remove(_mod); })
		.def("remove", [](Decimater& _self, ModQuadricHandle& _mod) { return _self.remove(_mod); })
		.def("remove", [](Decimater& _self, ModRoundnessHandle& _mod) { return _self.remove(_mod); })

		.def("module", [](Decimater& _self, ModAspectRatioHandle& _mod) -> ModAspectRatio& { return _self.module(_mod); }, py::return_value_policy::reference)
		.def("module", [](Decimater& _self, ModEdgeLengthHandle& _mod) -> ModEdgeLength& { return _self.module(_mod); }, py::return_value_policy::reference)
		.def("module", [](Decimater& _self, ModHausdorffHandle& _mod) -> ModHausdorff& { return _self.module(_mod); }, py::return_value_policy::reference)
		.def("module", [](Decimater& _self, ModIndependentSetsHandle& _mod) -> ModIndependentSets& { return _self.module(_mod); }, py::return_value_policy::reference)
		.def("module", [](Decimater& _self, ModNormalDeviationHandle& _mod) -> ModNormalDeviation& { return _self.module(_mod); }, py::return_value_policy::reference)
		.def("module", [](Decimater& _self, ModNormalFlippingHandle& _mod) -> ModNormalFlipping& { return _self.module(_mod); }, py::return_value_policy::reference)
		.def("module", [](Decimater& _self, ModProgMeshHandle& _mod) -> ModProgMesh& { return _self.module(_mod); }, py::return_value_policy::reference)
		.def("module", [](Decimater& _self, ModQuadricHandle& _mod) -> ModQuadric& { return _self.module(_mod); }, py::return_value_policy::reference)
		.def("module", [](Decimater& _self, ModRoundnessHandle& _mod) -> ModRoundness& { return _self.module(_mod); }, py::return_value_policy::reference)
		;

	// ModBase
	// ----------------------------------------

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModBase");

	py::class_<ModBase>(m, buffer)
		.def("name", &ModBase::name, py::return_value_policy::copy)
		.def("is_binary", &ModBase::is_binary)
		.def("set_binary", &ModBase::set_binary)
		.def("initialize", &ModBase::initialize) // TODO VIRTUAL
		.def("collapse_priority", &ModBase::collapse_priority) // TODO VIRTUAL
		.def("preprocess_collapse", &ModBase::preprocess_collapse) // TODO VIRTUAL
		.def("postprocess_collapse", &ModBase::postprocess_collapse) // TODO VIRTUAL
		.def("set_error_tolerance_factor", &ModBase::set_error_tolerance_factor) // TODO VIRTUAL
		;

	// ModAspectRatio
	// ----------------------------------------

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModAspectRatio");

	py::class_<ModAspectRatio, ModBase>(m, buffer)
		.def(py::init<Mesh&>(), py::keep_alive<1,2>())
		.def("aspect_ratio", &ModAspectRatio::aspect_ratio)
		.def("set_aspect_ratio", &ModAspectRatio::set_aspect_ratio)
		;

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModAspectRatioHandle");
	expose_module_handle<ModAspectRatioHandle>(m, buffer);

	// ModEdgeLength
	// ----------------------------------------

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModEdgeLength");

	py::class_<ModEdgeLength, ModBase>(m, buffer)
		.def(py::init<Mesh&>(), py::keep_alive<1,2>())
		.def("edge_length", &ModEdgeLength::edge_length)
		.def("set_edge_length", &ModEdgeLength::set_edge_length)
		;

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModEdgeLengthHandle");
	expose_module_handle<ModEdgeLengthHandle>(m, buffer);

	// ModHausdorff
	// ----------------------------------------

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModHausdorff");

	py::class_<ModHausdorff, ModBase>(m, buffer)
		.def(py::init<Mesh&>(), py::keep_alive<1,2>())
		.def("tolerance", &ModHausdorff::tolerance)
		.def("set_tolerance", &ModHausdorff::set_tolerance)
		;

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModHausdorffHandle");
	expose_module_handle<ModHausdorffHandle>(m, buffer);

	// ModIndependentSets
	// ----------------------------------------

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModIndependentSets");

	py::class_<ModIndependentSets, ModBase>(m, buffer)
		.def(py::init<Mesh&>(), py::keep_alive<1,2>())
		;

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModIndependentSetsHandle");
	expose_module_handle<ModIndependentSetsHandle>(m, buffer);

	// ModNormalDeviation
	// ----------------------------------------

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModNormalDeviation");

	py::class_<ModNormalDeviation, ModBase>(m, buffer)
		.def(py::init<Mesh&>(), py::keep_alive<1,2>())
		.def("normal_deviation", &ModNormalDeviation::normal_deviation)
		.def("set_normal_deviation", &ModNormalDeviation::set_normal_deviation)
		;

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModNormalDeviationHandle");
	expose_module_handle<ModNormalDeviationHandle>(m, buffer);

	// ModNormalFlipping
	// ----------------------------------------

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModNormalFlipping");

	py::class_<ModNormalFlipping, ModBase>(m, buffer)
		.def(py::init<Mesh&>(), py::keep_alive<1,2>())
		.def("max_normal_deviation", &ModNormalFlipping::max_normal_deviation)
		.def("set_max_normal_deviation", &ModNormalFlipping::set_max_normal_deviation)
		;

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModNormalFlippingHandle");
	expose_module_handle<ModNormalFlippingHandle>(m, buffer);

	// ModProgMesh
	// ----------------------------------------

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModProgMeshInfo");

	py::class_<Info>(m, buffer)
		.def_readwrite("v0", &Info::v0)
		.def_readwrite("v1", &Info::v1)
		.def_readwrite("vl", &Info::vl)
		.def_readwrite("vr", &Info::vr)
		;

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModProgMesh");

	py::class_<ModProgMesh, ModBase>(m, buffer)
		.def(py::init<Mesh&>(), py::keep_alive<1,2>())
		.def("pmi", &infolist<ModProgMesh>)
		.def("infolist", &infolist<ModProgMesh>)
		.def("write", &ModProgMesh::write)
		;

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModProgMeshHandle");
	expose_module_handle<ModProgMeshHandle>(m, buffer);

	// ModQuadric
	// ----------------------------------------

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModQuadric");

	py::class_<ModQuadric, ModBase>(m, buffer)
		.def(py::init<Mesh&>(), py::keep_alive<1,2>())
		.def("set_max_err", &ModQuadric::set_max_err,
			py::arg("err"), py::arg("binary")=true)
		.def("unset_max_err", &ModQuadric::unset_max_err)
		.def("max_err", &ModQuadric::max_err)
		;

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModQuadricHandle");
	expose_module_handle<ModQuadricHandle>(m, buffer);

	// ModRoundness
	// ----------------------------------------

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModRoundness");

	py::class_<ModRoundness, ModBase>(m, buffer)
		.def(py::init<Mesh&>(), py::keep_alive<1,2>())
		.def("set_min_angle", &ModRoundness::set_min_angle)
		.def("set_min_roundness", &ModRoundness::set_min_roundness,
			py::arg("min_roundness"), py::arg("binary")=true)
		.def("unset_min_roundness", &ModRoundness::unset_min_roundness)
		.def("roundness", &ModRoundness::roundness)
		;

	snprintf(buffer, sizeof buffer, "%s%s", _name, "ModRoundnessHandle");
	expose_module_handle<ModRoundnessHandle>(m, buffer);
}

#endif
