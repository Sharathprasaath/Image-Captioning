import React, { useState } from 'react';
import './page.css';
import axios from 'axios';
import utf8 from "utf8";
const BASE_URL = 'http://127.0.0.1:8000';
const encodeImage = async (image) => {
    try {
      console.log(image.slice(24))
      const response = await axios.post(`${BASE_URL}/image/caption`, {'image':utf8.decode(image.slice(23)) });
      console.log(response.data.image)
      return response.data.image;
    } catch (error) {
      console.error('Error encoding text:', error);
      return null;
    }
  };
function ImageCaptioning() { 
    const [image, setImage] = useState(null);
    const [caption, setCaption] = useState("");

    const handleDrop = (e) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = () => {
                setImage(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };
    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = () => {
                setImage(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
    };
   
    const handleGenerateCaption = async() => {
        let encoded = await encodeImage(image);

        setCaption(encoded);
    };
    const handleReset = () => {
        setImage(null);
        setCaption('')
    };

    return (
        <div className="container">
            <h1>Image Caption generator</h1>
            <div
                className="image-preview"
                style={{ backgroundImage: `url(${image})` }}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
            >
                {image ? null : <><p>Drag & Drop Image Here- </p>
                <label className="file-label" htmlFor="file-input"><p>-Choose File</p></label>
                        <input
                            id="file-input"
                            type="file"
                            accept="image/*"
                            onChange={handleFileChange}
                            style={{ display: 'none' }}
                        /></>}
                
            </div>
            {image && (
                <div className="button-container">
                <button onClick={handleGenerateCaption}>Generate Caption</button>
                <button onClick={handleReset} className="reset-button">Reset</button>
                </div>
            )}
            
            {caption && (
                <div className="caption">
                    <h2>Generated Caption:</h2>
                    <p>{caption}</p>
                </div>
            )}
        </div>
    );
}


export default ImageCaptioning;
