#version 330

// Input vertex attributes (from vertex shader)
in vec3 fragPosition;
in vec3 fragNormal;
in vec2 fragTexCoord;
in vec4 fragColor;

// Input uniform values
uniform sampler2D texture0;
uniform vec4 colDiffuse;

// Output fragment color
out vec4 finalColor;

// NOTE: Add your custom variables here

const float shininess = 16.0;
const float screenGamma = 2.2; // Assume the monitor is calibrated to the sRGB color space

// Input lighting values
uniform vec3 viewPos;
uniform vec3 lightPosition;
uniform vec4 lightColor;
uniform vec4 ambientColor;
uniform vec4 specularColor;

void main()
{
    // Texel color fetching from texture sampler
    vec4 texelColor = texture(texture0, fragTexCoord);

    // NOTE: Implement here your fragment shader code

    vec4 diffuseColor = colDiffuse * fragColor;

    vec3 normal = normalize(fragNormal);
    vec3 lightDir = normalize(lightPosition - fragPosition);

    float lambertian = max(dot(lightDir, normal), 0.0);

    float specular = 0.0;
    if (lambertian > 0.0) {
        vec3 viewDir = normalize(viewPos - fragPosition);
        specular = pow(max(dot(reflect(-lightDir, normal), viewDir), 0.0), shininess / 4.0);
    }

    finalColor = texelColor * (ambientColor + (diffuseColor * lambertian + specularColor * specular) * lightColor);

    // Gamma correction
    finalColor = pow(finalColor, vec4(1.0 / screenGamma));
}
