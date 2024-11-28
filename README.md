<a id="readme-top"></a>
<!-- PROJECT LOGO -->
#### Video Demo:  [https://youtu.be/W4Obx6zpRMc](https://youtu.be/W4Obx6zpRMc)
<br>
<div align="center">
  <a href="https://github.com/abdullah72005/Ultimate_Toolbox">
    <img src="static/imgs/iconpng.png" alt="Logo" width="100" height="100">
  </a>
<h1 align="center">Ultimate Toolbox</h1>
  <p align="center">
    A multipurpose toolbox offering file and image conversion, YouTube video and audio downloads, photo editing with filters, text and document translation, QR code generation, and password generation.
    <br />
    <a href="https://github.com/abdullah72005/Ultimate_Toolbox"><strong>Explore the docs »</strong></a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#conversion">Conversion</a></li>
        <li><a href="#youtube-downloader">Youtube Downloader</a></li>
        <li><a href="#photo-editor">Photo Editor</a></li>
        <li><a href="#translation">Translation</a></li>
        <li><a href="#qr-generator">Qr Generator</a></li>
        <li><a href="#password-generator">Password Generator</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Ultimate Toolbox Index Page][Ultimate-Toobox-index]
<br>
<br>
**Ultimate Toolbox** is a versatile software application designed to streamline and simplify your everyday tasks by providing a comprehensive suite of tools in one convenient platform. Whether you need to convert files and images, download videos and audio from YouTube, edit photos with filters, translate text and documents, generate QR codes, or create secure passwords, Ultimate Toolbox has you covered. The backend of the application is powered by Python's Flask framework, leveraging a variety of libraries to ensure efficient and robust functionality. The frontend is crafted with HTML, CSS, and JavaScript, offering a clean and user-friendly interface. Ultimate Toolbox is your go-to solution for enhancing productivity and managing tasks with ease.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With


* [![Python][Python-logo]][Python-url]
* [![Flask][Flask-logo]][Flask-url]
* [![HTML][HTML-logo]][HTML-url]
* [![CSS][CSS-logo]][CSS-url]
* [![JavaScript][JavaScript-logo]][JavaScript-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Conversion

The **Conversion** tool in Ultimate Toolbox provides a simple and efficient way to convert between a wide variety of file formats. Whether you need to work with images, audio files, datasheets, or documents, this tool ensures compatibility with multiple formats, helping you easily adapt your files for different uses. It also includes the option to convert images directly to PDF, streamlining the process of creating single-file documents from multiple images.


- **Supported Image Formats:** `bmp`, `gif`, `ico`, `jpeg`, `pcx`, `png`, `ppm`, `psd`, `tiff`, `webp`
- **Supported Audio Formats:** `wav`, `mp3`, `aac`, `m4a`, `ac3`, `amr`
- **Supported Datasheet Formats:** `csv`, `xlsx`, `json`
- **Supported Document Formats:** `docx`, `pdf`, `txt`

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Youtube Downloader

The **YouTube Downloader** tool in Ultimate Toolbox provides a straightforward solution for downloading YouTube videos and audio files. With this tool, you can easily extract high-quality content in your preferred format. It offers a variety of quality options for both video and audio, including HD and lower resolutions, so you can customize the downloads to fit your storage capacity or streaming needs.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Photo Editor


The **Photo Editor** tool in Ultimate Toolbox offers an easy-to-use interface for enhancing and personalizing your photos. With a variety of filters and editing options, you can quickly adjust your images to your liking.

#### Key Features:

- **Available Filters:** 
  - **Blur:** Softens the image for a dreamy or out-of-focus look.
  - **Contour:** Emphasizes edges and structure, adding depth.
  - **Detail:** Highlights textures and fine elements for clarity.
  - **Enhance:** Improves brightness, contrast, and sharpness.
  - **Emboss:** Creates a 3D, sculpted effect.
  - **Edge:** Highlights edges for a stylized, high-contrast effect.
  - **Sharpen:** Enhances image clarity by sharpening edges.
  - **Smooth:** Reduces noise for a polished, even look.

- **Available Editing Tools:**
  - **Rotation:** Adjust the image's orientation by any angle.
  - **Flipping:** Flip the image horizontally or vertically.
  - **Cropping:** Trim unwanted parts of the image to focus on key elements.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Translation

The **Translation** tool in Ultimate Toolbox provides powerful and seamless translation capabilities, allowing users to translate words, phrases, and entire documents between over 100 languages. It supports multiple file formats, including `docx` and `txt`, enabling users to easily convert the content of documents without losing formatting or accuracy.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Qr Generator

The **QR Generator** tool in Ultimate Toolbox allows you to create QR codes for a variety of inputs, such as URLs, text, or other data. This tool ensures accurate and reliable QR code generation, simplifying data sharing through scanning.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Password Generator

The **Password Generator** tool in Ultimate Toolbox provides a customizable way to create strong and secure passwords. It allows you to specify the password length and choose the components to include, such as lowercase letters, uppercase letters, numbers, and symbols. This ensures the generated passwords meet your security requirements and are tailored to your needs.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started



### Prerequisites

Before you begin, make sure you have Python3 installed. Then,
<br>

* Install Python libraries
  ```sh
  pip3 install flask flask-session Werkzeug Pillow python-docx PyPDF2 python-magic pydub pandas pyarrow openpyxl reportlab PyMuPDF pyqrcode pypng pytubefix googletrans pytube
  ```

* Install the alpha version of googletrans
  ```sh
  pip3 install googletrans==3.1.0a0
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/abdullah72005/Ultimate_Toolbox.git
   ```
2. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin abdullah72005/Ultimate_Toolbox
   git remote -v # confirm the changes
   ```
3. To start the application, execute:
   ```sh
   flask run
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Abdullah Hesham -
* Github: [@abdullah72005](https://github.com/abdullah72005) 
* Email: abdullahhesham005@gmail.com
* LinkedIn: [https://www.linkedin.com/in/abdullah-hesham-5043bb2b7/](https://www.linkedin.com/in/abdullah-hesham-5043bb2b7/) 

Ali Ehab -
* Github: [@Ali-2605](https://github.com/Ali-2605) 
* Email: ali.ehabezzeldin@gmail.com
* LinkedIn: [https://www.linkedin.com/in/ali-ehab-383716279](https://www.linkedin.com/in/ali-ehab-383716279) 

<br>

Project Link: [https://github.com/abdullah72005/Ultimate_Toolbox](https://github.com/abdullah72005/Ultimate_Toolbox)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Stack Overflow](https://stackoverflow.com/)
* [Pytubefix](https://github.com/JuanBindez/pytubefix)
* [Iconify](https://iconify.design/)
* [Googletrans API](https://py-googletrans.readthedocs.io/en/latest/)
* [Codepen](https://codepen.io/trending)
* [CS50 Duck Debugger](https://cs50.ai/chat)
* [Bootstrap](https://getbootstrap.com/)
* [Best README Template](https://github.com/othneildrew/Best-README-Template?tab=readme-ov-file#getting-started)
* [Color Picker](https://colorpicker.me/#ca12a9)
* [Choose an Open Source License](https://choosealicense.com)
* [Font Awesome](https://fontawesome.com)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Ultimate-Toobox-index]: static/imgs/indexSS.png
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[Python-logo]: https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Flask-logo]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/
[CSS-logo]: https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white
[CSS-url]: https://www.w3.org/Style/CSS/
[JavaScript-logo]: https://img.shields.io/badge/JavaScript-F7DF1C?style=for-the-badge&logo=javascript&logoColor=black
[JavaScript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript
[HTML-logo]: https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white
[HTML-url]: https://developer.mozilla.org/en-US/docs/Web/HTML
