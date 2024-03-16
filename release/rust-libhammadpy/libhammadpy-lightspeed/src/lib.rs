use pyo3::prelude::*;
use pyo3::types::{PyDict, PyTuple};
use rayon::prelude::*;
use std::sync::Arc;

#[pyclass]
struct Lightspeed {
    max_workers: Option<usize>,
}

#[pymethods]
impl Lightspeed {
    #[new]
    fn new(max_workers: Option<usize>) -> Self {
        Lightspeed { max_workers }
    }

    fn run(&self, py: Python, callable: PyObject, args: &PyTuple, kwargs: Option<&PyDict>) -> PyResult<PyObject> {
        let pool = rayon::ThreadPoolBuilder::new()
            .num_threads(self.max_workers.unwrap_or_else(num_cpus::get))
            .build()
            .unwrap();

        let callable = Arc::new(callable);
        let args = Arc::new(args.to_object(py));
        let kwargs = Arc::new(kwargs.map(|k| k.to_object(py)));

        let result = pool.install(|| {
            Python::with_gil(|py| {
                let callable = Arc::clone(&callable);
                let args = Arc::clone(&args);
                let kwargs = Arc::clone(&kwargs);

                py.allow_threads(move || {
                    let args = PyTuple::extract(args.as_ref(py)).unwrap();
                    let kwargs = kwargs
                        .as_ref()
                        .map(|k| PyDict::extract(k.as_ref(py)).unwrap());
                    callable.call(py, args, kwargs)
                })
            })
        })?;

        Ok(result)
    }

    fn multiplier(
        &self,
        py: Python,
        callable: PyObject,
        count: usize,
        args: &PyTuple,
        kwargs: Option<&PyDict>,
    ) -> PyResult<Vec<PyObject>> {
        let pool = rayon::ThreadPoolBuilder::new()
            .num_threads(self.max_workers.unwrap_or_else(num_cpus::get))
            .build()
            .unwrap();

        let callable = Arc::new(callable);
        let args = Arc::new(args.to_object(py));
        let kwargs = Arc::new(kwargs.map(|k| k.to_object(py)));

        let results = pool.install(|| {
            (0..count)
                .into_par_iter()
                .map(|_| {
                    Python::with_gil(|py| {
                        let callable = Arc::clone(&callable);
                        let args = Arc::clone(&args);
                        let kwargs = Arc::clone(&kwargs);

                        py.allow_threads(move || {
                            let args = PyTuple::extract(args.as_ref(py)).unwrap();
                            let kwargs = kwargs
                                .as_ref()
                                .map(|k| PyDict::extract(k.as_ref(py)).unwrap());
                            callable.call(py, args, kwargs)
                        })
                    })
                })
                .collect::<PyResult<Vec<PyObject>>>()
        })?;

        Ok(results)
    }
}

#[pymodule]
fn libhammadpy_lightspeed(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Lightspeed>()?;
    Ok(())
}