import { useState } from 'react';
import '../styles/ProfileSetup.css';

const ProfileSetup = ({ onComplete, onClose }) => {
  const [step, setStep] = useState(1);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    dob: '',
    gender: '',
    occupation: '',
    maritalStatus: '',
    familyDescription: '',
    neighborhood: ''
  });

  /* handle input change */

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });

    setError('');
  };

  /* next step */

  const nextStep = () => {
    /* step 1 */

    if (step === 1) {
      if (!formData.dob || !formData.gender || !formData.occupation.trim()) {
        setError('Please fill all required fields.');
        return;
      }
    }

    /* step 2 */

    if (step === 2) {
      if (!formData.maritalStatus || !formData.familyDescription.trim()) {
        setError('Please fill all required fields.');

        return;
      }
    }

    /* step 3 */

    if (step === 3) {
      if (!formData.neighborhood.trim()) {
        setError('Please describe familiar surroundings.');

        return;
      }
    }

    setError('');
    setStep((prev) => prev + 1);
  };

  /* PREVIOUS STEP */

  const prevStep = () => {
    setError('');
    setStep((prev) => prev - 1);
  };

  /* COMPLETE PROFILE */

  const handleComplete = async () => {
    try {
      setLoading(true);
      setError('');

      if (onComplete) {
        await onComplete([
          {
            dob: formData.dob,

            gender: formData.gender,

            occupation: formData.occupation.trim(),

            marital_status: formData.maritalStatus,

            family_description: formData.familyDescription.trim(),

            familiar_surroundings: formData.neighborhood.trim()
          }
        ]);
      }
    } catch (error) {
      console.error(error);
      setError(
        error?.response?.data?.error ||
          error?.response?.data?.detail ||
          error?.message ||
          'Failed to save patient profile.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="profile-overlay">
      <div className="profile-card">
        {/* close button */}

        <button className="profile-close-btn" onClick={() => onClose?.()} disabled={loading}>
          ×
        </button>

        {/* progress */}
        <div className="profile-progress">Step {step} of 4</div>

        {/* title */}
        <h2 className="profile-title">Complete Patient Profile</h2>

        {/* subtitle */}
        <p className="profile-subtitle">
          This information helps ReMIND personalize memory reconstruction.
        </p>

        {/* STEP 1 */}

        {step === 1 && (
          <div className="profile-form">
            <div className="profile-field">
              <label>Date of Birth</label>
              <input type="date" name="dob" value={formData.dob} onChange={handleChange} />
            </div>
            <div className="profile-field">
              <label>Gender</label>
              <select name="gender" value={formData.gender} onChange={handleChange}>
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div className="profile-field">
              <label>Occupation</label>
              <input
                type="text"
                name="occupation"
                placeholder="Former or current occupation"
                value={formData.occupation}
                onChange={handleChange}
              />
            </div>
          </div>
        )}

        {/* step 2 */}

        {step === 2 && (
          <div className="profile-form">
            <div className="profile-field">
              <label>Marital Status</label>
              <select name="maritalStatus" value={formData.maritalStatus} onChange={handleChange}>
                <option value="">Select Status</option>
                <option value="Single">Single</option>
                <option value="Married">Married</option>
                <option value="Widowed">Widowed</option>
                <option value="Divorced">Divorced</option>
              </select>
            </div>
            <div className="profile-field">
              <label>Family Description</label>
              <textarea
                name="familyDescription"
                placeholder="Tell us about family members, children, spouse, etc."
                value={formData.familyDescription}
                onChange={handleChange}
              />
            </div>
          </div>
        )}

        {/* step 3 */}

        {step === 3 && (
          <div className="profile-form">
            <div className="profile-field">
              <label>Familiar Surroundings</label>
              <textarea
                name="neighborhood"
                placeholder="Describe familiar surroundings, home, neighborhood, favorite places, etc."
                value={formData.neighborhood}
                onChange={handleChange}
              />
            </div>
          </div>
        )}

        {/* step 4 */}

        {step === 4 && (
          <div className="profile-complete">
            <div className="complete-icon">✓</div>
            <h3>Profile Ready</h3>
            <p>ReMIND will now personalize memory reconstruction using this information.</p>
          </div>
        )}

        {/* error */}
        {error && <p className="profile-error">{error}</p>}

        {/* actions */}
        <div className="profile-actions">
          {step > 1 && step < 4 && (
            <button className="profile-secondary-btn" onClick={prevStep} disabled={loading}>
              Back
            </button>
          )}

          {step < 3 && (
            <button className="profile-primary-btn" onClick={nextStep} disabled={loading}>
              Continue
            </button>
          )}

          {step === 3 && (
            <button className="profile-primary-btn" onClick={nextStep} disabled={loading}>
              Finish
            </button>
          )}

          {step === 4 && (
            <button className="profile-primary-btn" onClick={handleComplete} disabled={loading}>
              {loading ? 'Saving...' : 'Complete Setup'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
export default ProfileSetup;
