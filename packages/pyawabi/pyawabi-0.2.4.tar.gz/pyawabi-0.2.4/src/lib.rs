/*
*MIT License
*
*Copyright (c) 2020 Hajime Nakagami
*
*Permission is hereby granted, free of charge, to any person obtaining a copy
*of this software and associated documentation files (the "Software"), to deal
*in the Software without restriction, including without limitation the rights
*to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
*copies of the Software, and to permit persons to whom the Software is
*furnished to do so, subject to the following conditions:
*
*The above copyright notice and this permission notice shall be included in all
*copies or substantial portions of the Software.
*
*THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
*IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
*FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
*AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
*LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
*OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
*SOFTWARE.
*/
use awabi::tokenizer;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pyfunction]
fn tokenize(s: &str) -> PyResult<Vec<(String, String)>> {
    let tokenizer = tokenizer::Tokenizer::new(None).unwrap();
    Ok(tokenizer.tokenize(s))
}

#[pyfunction]
fn tokenize_n_best(s: &str, n: u32) -> PyResult<Vec<Vec<(String, String)>>> {
    let tokenizer = tokenizer::Tokenizer::new(None).unwrap();
    Ok(tokenizer.tokenize_n_best(s, n))
}

#[pyclass]
struct Tokenizer {
    inner: tokenizer::Tokenizer,
}

#[pymethods]
impl Tokenizer {
    #[new]
    fn new(mecabrc_path: Option<String>) -> Self {
        Tokenizer {
            inner: tokenizer::Tokenizer::new(mecabrc_path).unwrap(),
        }
    }

    pub fn tokenize(&self, s: &str) -> PyResult<Vec<(String, String)>> {
        Ok(self.inner.tokenize(s))
    }

    fn tokenize_n_best(&self, s: &str, n: u32) -> PyResult<Vec<Vec<(String, String)>>> {
        Ok(self.inner.tokenize_n_best(s, n))
    }
}

#[pymodule]
fn awabi(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(tokenize))?;
    m.add_wrapped(wrap_pyfunction!(tokenize_n_best))?;
    m.add_class::<Tokenizer>()?;
    Ok(())
}
