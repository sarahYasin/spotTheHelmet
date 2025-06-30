import React, { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);


  // get image and preview it
  const onDrop = (acceptedFiles) => {
    const file = acceptedFiles[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  // submit image and process it 
  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('image', image);
    setLoading(true);// to prevent submitting again and inturpting the following process
    try {
      // send to backend server for analyzing 
      const response = await axios.post('http://localhost:5000/process', formData);
      setResults(response.data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false); 
  };

  return (
    <div>
      <h2>Helmet Detection</h2>
      <div {...getRootProps()} style={{ border: '2px dashed black', padding: '20px' }}>
        <input {...getInputProps()} />
        <p>Drag & drop image here, or click to select</p>
      </div>
      {preview && <img src={preview} alt="preview" width="400" />}
      <button onClick={handleSubmit} disabled={!image || loading}>Submit</button>
      {loading && <p>Loading...</p>}
      {results && ( // show results
        <>
          <img src={`data:image/jpeg;base64,${results.image}`} width="400" alt="Result" />
          <ul>
            {results.metadata.map((item, index) => (
              <li key={index}>
                Person {index + 1}: {item.helmet ? 'With Helmet' : 'Without Helmet'}
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default App;